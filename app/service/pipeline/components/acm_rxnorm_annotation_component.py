from typing import List, Dict

from app.dto.core.medical_ontology import MedicalOntology
from app.dto.core.pipeline.acm_rxnorm_response import ACMRxNormResult
from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.pipeline.rxnorm_annotation_result import RxNormAnnotationResult
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.rxnorm_annotator_service import RxNormAnnotatorService
from app.service.impl.amazon_rxnorm_annotator_service import AmazonRxNormAnnotatorServiceImpl
from app.service.impl.dynamo_db_service import DynamoDbService
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.util.annotations_alignment_util import AnnotationAlignmentUtil
from app.util.config_manager import ConfigManager
from app.util.dependency_injector import DependencyInjector


class ACMRxNormAnnotationComponent(BasePipelineComponent):
    DEPENDS_ON: List = [NegationHandlingComponent, NotePreprocessingComponent]

    def __init__(self):
        super().__init__()

        self.__rxnorm_annotation_service: RxNormAnnotatorService = DependencyInjector.get_instance(
            AmazonRxNormAnnotatorServiceImpl)

        self.__note_to_align: str = MedicalOntology.RXNORM.value

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
        AnnotationAlignmentUtil.align_start_and_end_notes_from_annotations(self.__note_to_align, result,
                                                                           annotation_results)

        self.__db_service.save_item(result)
        return [result]
