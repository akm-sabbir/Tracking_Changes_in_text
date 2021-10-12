from typing import List

from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.icd10_annotator_service_with_filters import ICD10AnnotatorServiceWithFilter
from app.service.impl import icd10_annotator_service_with_filters_impl
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.icd10_annotation_component import ICD10AnnotationComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.util.dependency_injector import DependencyInjector


class ICD10AnnotationComponent(BasePipelineComponent):
    DEPENDS_ON: List = [NotePreprocessingComponent, ICD10AnnotationComponent]

    def __init__(self):
        super().__init__()
        self.__icd10_annotation_service_with_filters: ICD10AnnotatorServiceWithFilter = \
            DependencyInjector.get_instance(icd10_annotator_service_with_filters_impl)

    def run(self, annotation_results: dict) -> List[ICD10AnnotationResult]:
        icd10AnnotationResult: List[ICD10AnnotationResult] = annotation_results[ICD10AnnotationComponent]
        dx_threshold = annotation_results['dx_threshold']
        icd10_threshold = annotation_results['icd10_threshold']
        parent_threshold = annotation_results['parent_threshold']
        filtered_results = self.__icd10_annotation_service_with_filters.get_icd_10_filtered_codes(icd10AnnotationResult,
                                                                               dx_threshold=dx_threshold,
                                                                               icd10_threshold=icd10_threshold,
                                                                               parent_threshold=parent_threshold)

        return filtered_results
