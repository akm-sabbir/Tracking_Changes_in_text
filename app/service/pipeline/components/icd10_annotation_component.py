from typing import List

from app.dto.core.paragraph import Paragraph
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.icd10_annotator_service import ICD10AnnotatorService
from app.service.impl.amazon_icd10_annotator_service import AmazonICD10AnnotatorServiceImpl
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.util.dependency_injector import DependencyInjector


class ICD10AnnotationComponent(BasePipelineComponent):
    DEPENDS_ON: List = [NotePreprocessingComponent]

    def __init__(self):
        super().__init__()
        self.__icd10_annotation_service: ICD10AnnotatorService = DependencyInjector.get_instance(
            AmazonICD10AnnotatorServiceImpl)

    def run(self, annotation_results: dict) -> List[ICD10AnnotationResult]:
        paragraphs: List[Paragraph] = annotation_results[NotePreprocessingComponent]
        annotation_result_set = []

        for paragraph in paragraphs:
            annotations: List[ICD10AnnotationResult] = self.__icd10_annotation_service.get_icd_10_codes(paragraph.text)
            for annotation in annotations:
                annotation.begin_offset += paragraph.start_index
                annotation.end_offset += paragraph.start_index
            annotation_result_set += annotations

        return annotation_result_set
