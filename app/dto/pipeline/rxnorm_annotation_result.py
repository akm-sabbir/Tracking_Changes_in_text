from typing import Optional, List

from app.dto.base_dto import BaseDto
from app.dto.pipeline.rxnorm_annotation import RxNormAnnotation
from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class RxNormAnnotationResult(BaseDto, BasePipelineComponentResult):
    medication: str
    score: Optional[float]
    begin_offset: int
    end_offset: int
    is_negated: bool
    suggested_codes: List[RxNormAnnotation]
