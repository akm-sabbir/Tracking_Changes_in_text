from typing import List

from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult


class ACMICD10Result(BasePipelineComponentResult):
    id: str
    icd10_annotations: List[ICD10AnnotationResult]

    def __init__(self, note_id: str, icd10_annotations: List[ICD10AnnotationResult]):
        self.id = note_id
        self.icd10_annotations = icd10_annotations
