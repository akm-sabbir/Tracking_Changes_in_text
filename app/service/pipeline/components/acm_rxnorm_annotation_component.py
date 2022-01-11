import re
from typing import List, Dict

from app.dto.core.pipeline.acm_rxnorm_response import ACMRxNormResult
from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.pipeline.medication_section import MedicationText
from app.dto.pipeline.rxnorm_annotation_result import RxNormAnnotationResult
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.rxnorm_annotator_service import RxNormAnnotatorService
from app.service.impl.amazon_rxnorm_annotator_service import AmazonRxNormAnnotatorServiceImpl
from app.service.impl.dynamo_db_service import DynamoDbService
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.util.config_manager import ConfigManager
from app.util.dependency_injector import DependencyInjector


class ACMRxNormAnnotationComponent(BasePipelineComponent):
    DEPENDS_ON: List = [NegationHandlingComponent, NotePreprocessingComponent]

    def __init__(self):
        super().__init__()

        self.__rxnorm_annotation_service: RxNormAnnotatorService = DependencyInjector.get_instance(
            AmazonRxNormAnnotatorServiceImpl)

        self.__db_service = DynamoDbService(ConfigManager.get_specific_config("aws", "annotation_table_name"))

    def run(self, annotation_results: dict) -> List[ACMRxNormResult]:
        if annotation_results['acm_cached_result'] is not None:
            return []

        paragraphs: List[Paragraph] = annotation_results[NotePreprocessingComponent][1]

        rxnorm_annotation_results: List[RxNormAnnotationResult] = []
        raw_acm_data: List[Dict] = []
        for paragraph in paragraphs:
            if not paragraph.text == "":
                acm_data, annotations = self.__rxnorm_annotation_service.get_rxnorm_codes(paragraph.text)
                raw_acm_data.extend(acm_data)
                for annotation in annotations:
                    annotation.begin_offset += paragraph.start_index
                    annotation.end_offset += paragraph.start_index
                rxnorm_annotation_results += annotations

        result = ACMRxNormResult(annotation_results["id"], rxnorm_annotation_results, raw_acm_data)
        self.align_start_and_text(result, annotation_results[MedicationSectionExtractorComponent][0].text,
                                  annotation_results[NegationHandlingComponent][1].text,
                                  annotation_results['changed_words'])

        self.align_start_end_for_medication_part(result, annotation_results[MedicationSectionExtractorComponent][0], annotation_results)
        self.__db_service.save_item(result)
        return [result]

    def align_start_and_text(self, acm_result: ACMRxNormResult, original_text: str, changed_text: str,
                             changed_words: dict):

        for annotation in acm_result.rxnorm_annotations:
            annotation_text = annotation.medication
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
            annotation.medication = matches[match_index].group()
            return True
        else:
            return False

    def align_start_end_for_medication_part(self, acm_result: ACMRxNormResult, medication_text: MedicationText, annotation_results):
        sections = medication_text.medication_sections
        section_index = 0
        annotation_index = 0
        acm_result.rxnorm_annotations.sort(key=lambda x: x.begin_offset)

        while not annotation_index == len(acm_result.rxnorm_annotations):
            annotation = acm_result.rxnorm_annotations[annotation_index]
            current_section = sections[section_index]
            if annotation.begin_offset >= current_section.relative_start and annotation.end_offset <= current_section.relative_end:
                annotation.begin_offset = annotation.begin_offset - current_section.relative_start + current_section.start
                annotation.end_offset = annotation.end_offset - current_section.relative_start + current_section.start
                annotation_index = annotation_index + 1
            else:
                section_index = section_index + 1
