from typing import List

from app.dto.core.pipeline.acm_icd10_response import ICD10Result
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.service.impl.icd10_annotation_service_with_filters_impl import ICD10AnnotatorServiceWithFilterImpl
from app.service.pipeline.components.acmscimetamap_icd10_annotation_component import ICD10AnnotationComponent
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.icd10_to_hcc_annotation import ICD10ToHccAnnotationComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.util.dependency_injector import DependencyInjector
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.icd10_exclusion_list_processing_component import CodeExclusionHandlingComponent


class ICD10AnnotationAlgoComponent(BasePipelineComponent):
    DEPENDS_ON: List = [NegationHandlingComponent, NotePreprocessingComponent,
                        ICD10AnnotationComponent, ICD10ToHccAnnotationComponent, CodeExclusionHandlingComponent]

    def __init__(self):
        super().__init__()
        self.__icd10_annotation_service_with_filters: ICD10AnnotatorServiceWithFilterImpl = \
            DependencyInjector.get_instance(ICD10AnnotatorServiceWithFilterImpl)

    def run(self, annotation_results: dict) -> List[ICD10AnnotationResult]:
        icd10_result: ICD10Result = annotation_results[ICD10AnnotationComponent]
        icd10_annotation_result: List[ICD10AnnotationResult] = icd10_result[0].icd10_annotations
        hcc_result: HCCResponseDto = annotation_results[ICD10ToHccAnnotationComponent][0].hcc_annotation_response
        hcc_mapping: dict = hcc_result.hcc_maps

        dx_threshold = annotation_results['dx_threshold']
        icd10_threshold = annotation_results['icd10_threshold']
        parent_threshold = annotation_results['parent_threshold']
        filtered_results = self.__icd10_annotation_service_with_filters.get_icd_10_filtered_codes \
            (icd10_annotation_result, hcc_map=hcc_mapping if hcc_mapping is not None else {},
             dx_threshold=dx_threshold,
             icd10_threshold=icd10_threshold,
             parent_threshold=parent_threshold)

        return filtered_results
