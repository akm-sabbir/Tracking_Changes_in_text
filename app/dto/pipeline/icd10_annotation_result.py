from typing import List, Optional

from app.dto.base_dto import BaseDto
from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult
from app.dto.pipeline.icd10_annotation import ICD10Annotation


class ICD10AnnotationResult(BaseDto, BasePipelineComponentResult):
    medical_condition: str
    score: Optional[float]
    begin_offset: int
    end_offset: int
    is_negated: bool
    suggested_codes: List[ICD10Annotation]