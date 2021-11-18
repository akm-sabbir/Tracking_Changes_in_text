from typing import List

from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.request.hcc_request_dto import HCCRequestDto
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.service.hcc_service import HCCService
from app.service.impl.hcc_service_impl import HCCServiceImpl
from app.service.pipeline.components.acm_icd10_annotation_component import ACMICD10AnnotationComponent
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.icd10_annotation_filter_component import ICD10AnnotationAlgoComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent


class FilteredICD10ToHccAnnotationComponent(BasePipelineComponent):
    DEPENDS_ON: List = [NegationHandlingComponent, NotePreprocessingComponent, ACMICD10AnnotationComponent,
                        ICD10AnnotationAlgoComponent]

    def __init__(self):
        super().__init__()
        self.__hcc_service: HCCService = HCCServiceImpl()

    def run(self, annotation_results: dict) -> List[HCCResponseDto]:
        annotated_list: List[ICD10AnnotationResult] = annotation_results[ICD10AnnotationAlgoComponent]
        all_icd10_annotations = []

        for annotation_entity in annotated_list:
            annotations: List[str] = [icd10.code for icd10 in annotation_entity.suggested_codes]
            all_icd10_annotations.extend(annotations)
        hcc_request = HCCRequestDto(icd_codes_list=all_icd10_annotations)
        hcc_annotation: HCCResponseDto = self.__hcc_service.get_hcc_risk_scores(hcc_request)
        return [hcc_annotation]
