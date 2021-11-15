from typing import List

from app.dto.core.pipeline.acm_icd10_response import ACMICD10Result
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.request.hcc_request_dto import HCCRequestDto
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.service.hcc_service import HCCService
from app.service.impl.hcc_service_impl import HCCServiceImpl
from app.service.pipeline.components.acm_icd10_annotation_component import ACMICD10AnnotationComponent
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from collections import namedtuple
from app.dto.pipeline.icd10_meta_info import icd10_meta_info


class ICD10ToHccAnnotationComponent(BasePipelineComponent):
    DEPENDS_ON: List = [NegationHandlingComponent, NotePreprocessingComponent, ACMICD10AnnotationComponent]

    def __init__(self):
        super().__init__()
        self.__hcc_service: HCCService = HCCServiceImpl()

    def run(self, annotation_results: dict) -> List[HCCResponseDto]:
        acm_result: List[ACMICD10Result] = annotation_results[ACMICD10AnnotationComponent]
        annotated_list: List[ICD10AnnotationResult] = acm_result[0].icd10_annotations
        all_icd10_annotations = []
        icd10_metadata_map = dict()
        for annotation_entity in annotated_list:
            annotations: List[str] = list()
            for icd10 in annotation_entity.suggested_codes:
                annotations.append(icd10.code)
                icd10_metadata_map[icd10.code.replace(".", "")] = icd10_meta_info()
                icd10_meta_info.score = icd10.score
                icd10_meta_info.length = len(icd10.code.replace(".", ""))
                icd10_meta_info.entity_score = annotation_entity.score
            all_icd10_annotations.extend(annotations)
        hcc_request = HCCRequestDto(icd_codes_list=all_icd10_annotations)
        hcc_annotation: HCCResponseDto = self.__hcc_service.get_hcc_risk_scores(hcc_request)
        for key, values in hcc_annotation.hcc_maps.items():
            icd10_metadata_map[key].hcc_map = values
        return [hcc_annotation, icd10_metadata_map]
