from typing import Optional, List

from app.dto.base_dto import BaseDto
from app.dto.pipeline.rxnorm_annotation import RxNormAnnotation
from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult
from app.dto.pipeline.rxnorm_attribute_annotation import RxNormAttributeAnnotation


class RxNormAnnotationResult(BaseDto, BasePipelineComponentResult):
    medication: str
    rxnorm_type: str
    attributes: List[RxNormAttributeAnnotation]
    score: Optional[float]
    begin_offset: int
    end_offset: int
    is_negated: bool
    suggested_codes: List[RxNormAnnotation]
