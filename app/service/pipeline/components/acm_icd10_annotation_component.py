import re
from typing import List, Dict

from app.dto.core.pipeline.acm_icd10_response import ACMICD10Result
from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.icd10_annotator_service import ICD10AnnotatorService
from app.service.impl.amazon_icd10_annotator_service import AmazonICD10AnnotatorServiceImpl
from app.service.impl.dynamo_db_service import DynamoDbService
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.util.config_manager import ConfigManager
from app.util.dependency_injector import DependencyInjector


class ACMICD10AnnotationComponent(BasePipelineComponent):
    DEPENDS_ON: List = [NegationHandlingComponent, NotePreprocessingComponent]

    def __init__(self):
        super().__init__()
        self.__icd10_annotation_service: ICD10AnnotatorService = DependencyInjector.get_instance(
            AmazonICD10AnnotatorServiceImpl)
        self.__db_service = DynamoDbService(ConfigManager.get_specific_config("aws", "annotation_table_name"))

    def run(self, annotation_results: dict) -> List[ACMICD10Result]:
        if annotation_results['acm_cached_result'] is not None:
            self.align_start_and_text(annotation_results['acm_cached_result'][0], annotation_results['text'])
            return annotation_results['acm_cached_result']
        paragraphs: List[Paragraph] = annotation_results[NotePreprocessingComponent]

        icd10_annotation_results: List[ICD10AnnotationResult] = []
        raw_acm_data: List[Dict] = []
        for paragraph in paragraphs:
            acm_data, annotations = self.__icd10_annotation_service.get_icd_10_codes(paragraph.text)
            raw_acm_data.extend(acm_data)
            for annotation in annotations:
                annotation.begin_offset += paragraph.start_index
                annotation.end_offset += paragraph.start_index
            icd10_annotation_results += annotations
        result = ACMICD10Result(annotation_results["id"], icd10_annotation_results, raw_acm_data)
        self.align_start_and_text(result, annotation_results['text'])
        self.__db_service.save_item(result)
        return [result]

    def align_start_and_text(self, acm_result: ACMICD10Result, original_text: str):

        for annotation in acm_result.icd10_annotations:
            annotation_text = annotation.medical_condition
            word_list = re.sub(r"[^\w]", " ", annotation_text).split()
            consecutive_words_match_regex = r"[^\w]*?".join(word_list)

            """ if annotation_text is "high fever" then consecutive_words_match_regex is "high[^\w]*?fever", 
            it matches words present annotation_text consecutively in original text """

            matches = [match for match in re.finditer(consecutive_words_match_regex, original_text, re.IGNORECASE)]
            min_distance = len(original_text)
            match_index = 0
            if len(matches) == 0:
                continue
            for index, match in enumerate(matches):
                distance = abs(match.start() - annotation.begin_offset)
                if distance < min_distance:
                    min_distance = distance
                    match_index = index
            annotation.begin_offset = matches[match_index].start()
            annotation.end_offset = matches[match_index].end()
            annotation.medical_condition = matches[match_index].group()
