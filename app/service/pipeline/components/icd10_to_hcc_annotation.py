from typing import List

from app.dto.core.pipeline.acm_icd10_response import ICD10Result
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.pipeline.icd10_meta_info import ICD10MetaInfo
from app.dto.request.hcc_request_dto import HCCRequestDto
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.service.hcc_service import HCCService
from app.service.impl.hcc_service_impl import HCCServiceImpl
from app.service.pipeline.components.acmscimetamap_icd10_annotation_component import ICD10AnnotationComponent
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.dto.pipeline.icd10_hcc_meta_info import Icd10HccMeta


class ICD10ToHccAnnotationComponent(BasePipelineComponent):
    DEPENDS_ON: List = [NegationHandlingComponent, NotePreprocessingComponent, ICD10AnnotationComponent]

    def __init__(self):
        super().__init__()
        self.__hcc_service: HCCService = HCCServiceImpl()

    def run(self, annotation_results: dict) -> List[Icd10HccMeta]:
        icd10_result: List[ICD10Result] = annotation_results[ICD10AnnotationComponent]
        annotated_list: List[ICD10AnnotationResult] = icd10_result[0].icd10_annotations
        all_icd10_annotations = []
        icd10_metadata_map = dict()
        for annotation_entity in annotated_list:
            annotations: List[str] = list()
            for icd10 in annotation_entity.suggested_codes:
                annotations.append(icd10.code)
                icd10_metadata_map[icd10.code.replace(".", "")] = ICD10MetaInfo(
                    score=icd10.score, length=len(icd10.code.replace(".", "")))
            all_icd10_annotations.extend(annotations)
        hcc_request = HCCRequestDto(icd_codes_list=all_icd10_annotations)
        hcc_annotation: HCCResponseDto = self.__hcc_service.get_hcc_risk_scores(hcc_request)
        for key, values in hcc_annotation.hcc_maps.items():
            icd10_metadata_map[key].hcc_map = values.code
        annotated_results = Icd10HccMeta(hcc_annotation, icd10_metadata_map)
        return [annotated_results]
