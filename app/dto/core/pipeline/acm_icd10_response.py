from typing import List, Dict

from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult


class ACMICD10Result(BasePipelineComponentResult):
    def __init__(self, note_id: str, icd10_annotations: List[ICD10AnnotationResult], raw_acm_data: List[Dict]):
        self.id: str = note_id
        self.icd10_annotations: List[ICD10AnnotationResult] = icd10_annotations
        self.raw_acm_data: List[Dict] = raw_acm_data
