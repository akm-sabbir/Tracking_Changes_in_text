import re
from typing import List, Dict

from app.dto.core.pipeline.acm_icd10_response import ACMICD10Result
from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.pipeline.subjective_section import SubjectiveText
from app.service.icd10_annotator_service import ICD10AnnotatorService
from app.service.icd10_positive_sentiment_exclusion_service import ICD10SentimentExclusionService
from app.service.impl.amazon_icd10_annotator_service import AmazonICD10AnnotatorServiceImpl
from app.service.impl.dynamo_db_service import DynamoDbService
from app.service.impl.icd10_positive_sentiment_exclusion_service_impl import ICD10SentimentExclusionServiceImpl
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.service.pipeline.components.section_exclusion_service_component import SectionExclusionServiceComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.util.config_manager import ConfigManager
from app.util.dependency_injector import DependencyInjector
from app.util.icd_10_filter_util import ICD10FilterUtil


class ACMICD10AnnotationComponent(BasePipelineComponent):
    DEPENDS_ON: List = [NegationHandlingComponent, NotePreprocessingComponent]

    def __init__(self):
        super().__init__()
        self.__icd10_annotation_service: ICD10AnnotatorService = DependencyInjector.get_instance(
            AmazonICD10AnnotatorServiceImpl)

        self.__icd10_positive_sentiment_exclusion_service: ICD10SentimentExclusionService = DependencyInjector.get_instance(
            ICD10SentimentExclusionServiceImpl)

        self.__db_service = DynamoDbService(ConfigManager.get_specific_config("aws", "annotation_table_name"))

    def run(self, annotation_results: dict) -> List[ACMICD10Result]:
        if annotation_results['acm_cached_result'] is not None:
            return annotation_results['acm_cached_result']
        paragraphs: List[Paragraph] = annotation_results[NotePreprocessingComponent][0]

        icd10_annotation_results: List[ICD10AnnotationResult] = []
        raw_acm_data: List[Dict] = []
        for paragraph in paragraphs:
            if not paragraph.text == "":
                acm_data, annotations = self.__icd10_annotation_service.get_icd_10_codes(paragraph.text)
                raw_acm_data.extend(acm_data)
                for annotation in annotations:
                    annotation.begin_offset += paragraph.start_index
                    annotation.end_offset += paragraph.start_index
                icd10_annotation_results += annotations

        filtered_icd10_annotations_from_sentiment = self.__icd10_positive_sentiment_exclusion_service.get_filtered_annotations_based_on_positive_sentiment(
            icd10_annotation_results)

        filtered_icd10_annotations_from_excluded_sections = ICD10FilterUtil.get_filtered_annotations_based_on_excluded_sections(
            filtered_icd10_annotations_from_sentiment, annotation_results[SectionExclusionServiceComponent]
        )

        result = ACMICD10Result(annotation_results["id"], filtered_icd10_annotations_from_excluded_sections, raw_acm_data)
        self.align_start_and_text(result, annotation_results[SubjectiveSectionExtractorComponent][0].text,
                                  annotation_results[NegationHandlingComponent][0].text,
                                  annotation_results['changed_words'])

        self.align_start_end_for_subjective_part(result, annotation_results[SubjectiveSectionExtractorComponent][0])
        self.__db_service.save_item(result)
        return [result]

    def align_start_and_text(self, acm_result: ACMICD10Result, original_text: str, changed_text: str,
                             changed_words: dict):

        for annotation in acm_result.icd10_annotations:
            annotation_text = annotation.medical_condition
            word_list = re.sub(r"[^\w]", " ", annotation_text).split()

            match_found = self._reassign_acm_annotation_values(annotation, word_list, original_text, changed_text)

            if match_found:
                continue

            changed_word_list = []
            for idx, word in enumerate(word_list):
                if word in changed_words:
                    changed_word_list.append(
                        "|".join([changed_word.original_text for changed_word in changed_words[word]]))
                else:
                    changed_word_list.append(word)

            consecutive_words_match_regex_changed = r"[^\w]*?".join(changed_word_list)
            self._reassign_acm_annotation_values(annotation, word_list, original_text, changed_text,
                                                 consecutive_words_match_regex_changed)

    def _reassign_acm_annotation_values(self, annotation, words_list: List, original_text: str, changed_text: str,
                                        consecutive_words_match_regex_changed: str = None):

        """ if annotation_text is "high fever" then consecutive_words_match_regex is "high[^\w]*?fever",
                       it matches words present annotation_text consecutively in original text """

        consecutive_words_match_regex = r"[^\w]*?".join(words_list)
        matches_changed = [match for match in
                           re.finditer(consecutive_words_match_regex, changed_text, re.IGNORECASE)]

        if consecutive_words_match_regex_changed:
            consecutive_words_match_regex = consecutive_words_match_regex_changed

        matches = [match for match in re.finditer(consecutive_words_match_regex, original_text, re.IGNORECASE)]

        match_index = 0
        match_found = False
        for idx, match in enumerate(matches_changed):
            if match.start() == annotation.begin_offset and match.end() == annotation.end_offset:
                match_index = idx
                match_found = True
                break

        if match_found and len(matches) > match_index:
            annotation.begin_offset = matches[match_index].start()
            annotation.end_offset = matches[match_index].end()
            annotation.medical_condition = matches[match_index].group()
            return True
        else:
            return False

    def align_start_end_for_subjective_part(self, acm_result: ACMICD10Result, subjective_text: SubjectiveText):
        sections = subjective_text.subjective_sections
        section_index = 0
        annotation_index = 0
        acm_result.icd10_annotations.sort(key=lambda x: x.begin_offset)

        while not annotation_index == len(acm_result.icd10_annotations):
            annotation = acm_result.icd10_annotations[annotation_index]
            current_section = sections[section_index]
            if annotation.begin_offset >= current_section.relative_start and annotation.end_offset <= current_section.relative_end:
                annotation.begin_offset = annotation.begin_offset - current_section.relative_start + current_section.start
                annotation.end_offset = annotation.end_offset - current_section.relative_start + current_section.start
                annotation_index = annotation_index + 1
            else:
                section_index = section_index + 1
