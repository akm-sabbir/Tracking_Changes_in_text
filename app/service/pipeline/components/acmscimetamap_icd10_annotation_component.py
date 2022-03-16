from typing import List, Dict

from app.dto.core.icd10_algorithm_constants import ICD10Algorithm
from app.dto.core.medical_ontology import MedicalOntology
from app.dto.core.pipeline.icd10_result import ICD10Result
from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.icd10_annotator_service import ICD10AnnotatorService
from app.service.icd10_positive_sentiment_exclusion_service import ICD10SentimentExclusionService
from app.service.impl.amazon_icd10_annotator_service import AmazonICD10AnnotatorServiceImpl
from app.service.impl.dynamo_db_service import DynamoDbService
from app.service.impl.icd10_positive_sentiment_exclusion_service_impl import ICD10SentimentExclusionServiceImpl
from app.service.impl.pymetamap_icd10_annotator_service import PymetamapICD10AnnotatorService
from app.service.impl.scispacy_icd10_annotator_service import ScispacyICD10AnnotatorService
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.service.pipeline.components.section_exclusion_service_component import SectionExclusionServiceComponent
from app.util.annotations_alignment_util import AnnotationAlignmentUtil
from app.util.config_manager import ConfigManager
from app.util.dependency_injector import DependencyInjector
from app.util.icd_10_filter_util import ICD10FilterUtil
from app.util.span_merger_util import SpanMergerUtil


class ACMSciMetamapICD10AnnotationComponent(BasePipelineComponent):
    DEPENDS_ON: List = [NegationHandlingComponent, NotePreprocessingComponent]

    def __init__(self):
        super().__init__()
        self.__acm_icd10_annotation_service: ICD10AnnotatorService = DependencyInjector.get_instance(
            AmazonICD10AnnotatorServiceImpl)

        self.__note_to_align: str = MedicalOntology.ICD10_CM.value
        self.__no_of_components_in_icd10_algorithm = ICD10Algorithm.NO_OF_COMPONENTS.value

        self.__icd10_positive_sentiment_exclusion_service: ICD10SentimentExclusionService = DependencyInjector.get_instance(
            ICD10SentimentExclusionServiceImpl)

        self.__scispacy_annotation_service: ICD10AnnotatorService = DependencyInjector.get_instance(
            ScispacyICD10AnnotatorService)
        self.__metamap_annotation_service: ICD10AnnotatorService = DependencyInjector.get_instance(
            PymetamapICD10AnnotatorService)

        self.__db_service = DynamoDbService(ConfigManager.get_specific_config("aws", "annotation_table_name"))

    def run(self, annotation_results: dict) -> List[ICD10Result]:
        if annotation_results['acm_cached_result'] is not None:
            return annotation_results['acm_cached_result']
        paragraphs: List[Paragraph] = annotation_results[NotePreprocessingComponent][0]

        icd10_annotation_results: List[ICD10AnnotationResult] = []
        raw_acm_data: List[Dict] = []
        for paragraph in paragraphs:
            if not paragraph.text == "":
                acm_data, acm_annotations = self.__acm_icd10_annotation_service.get_icd_10_codes(paragraph.text)
                raw_acm_data.extend(acm_data)

                scispacy_predictions = self.__scispacy_annotation_service.get_icd_10_codes(paragraph.text)
                metamap_predictions = self.__metamap_annotation_service.get_icd_10_codes(paragraph.text)

                annotations = acm_annotations + scispacy_predictions + metamap_predictions

                for annotation in annotations:
                    annotation.begin_offset += paragraph.start_index
                    annotation.end_offset += paragraph.start_index
                icd10_annotation_results += annotations

        filtered_icd10_annotations_from_sentiment = self.__icd10_positive_sentiment_exclusion_service.get_filtered_annotations_based_on_positive_sentiment(
            icd10_annotation_results)

        filtered_icd10_annotations_from_excluded_sections = ICD10FilterUtil.get_filtered_annotations_based_on_excluded_sections(
            filtered_icd10_annotations_from_sentiment, annotation_results[SectionExclusionServiceComponent]
        )

        result = ICD10Result(annotation_results["id"], filtered_icd10_annotations_from_excluded_sections,
                             raw_acm_data)
        AnnotationAlignmentUtil.align_start_and_end_notes_from_annotations(self.__note_to_align, result,
                                                                           annotation_results)

        # exclude negated
        result.icd10_annotations = [annotation for annotation in result.icd10_annotations if
                                    annotation.is_negated is False]

        # merge the spans
        result.icd10_annotations = SpanMergerUtil.get_icd_10_codes_with_relevant_spans(
            result.icd10_annotations, self.__no_of_components_in_icd10_algorithm
        )

        self.__db_service.save_item(result)

        return [result]
