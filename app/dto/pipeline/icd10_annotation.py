from typing import Optional

from app.dto.base_dto import BaseDto
from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class ICD10Annotation(BaseDto, BasePipelineComponentResult):
    code: str
    description: str
    score: Optional[float] = 0
