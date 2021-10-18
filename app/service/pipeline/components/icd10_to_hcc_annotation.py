from typing import List

from app.dto.core.paragraph import Paragraph
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.icd10_annotator_service import ICD10AnnotatorService
from app.service.impl.amazon_icd10_annotator_service import AmazonICD10AnnotatorServiceImpl
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.util.dependency_injector import DependencyInjector
from app.service.pipeline.components.icd10_annotation_component import ICD10AnnotationComponent
from hccpy.hcc import HCCEngine


class ICD10ToHccAnnotationComponent(BasePipelineComponent):
    DEPENDS_ON: List = [NotePreprocessingComponent, ICD10AnnotationComponent]

    def __init__(self):
        super().__init__()
        self.__hcc_service: ICD10AnnotatorService = HCCEngine(version="23")

    def run(self, annotation_results: dict) -> dict:
        annotated_list: List[ICD10AnnotationResult] = annotation_results[ICD10AnnotationComponent]
        annotation_result_set = {}

        for annotation_entity in annotated_list:
            annotations: List[ICD10Annotation] = self.get_icd10_list(annotation_entity)
            hcc_annotation: dict = self.__hcc_service.profile(dx_lst=annotations)
            if hcc_annotation.get('hcc_map') is not None:
                annotation_result_set.update(hcc_annotation)

        return annotation_result_set

    def get_icd10_list(self, annotation_entity: ICD10AnnotationResult):
        return [each_ob.code for each_ob in annotation_entity.suggested_codes]