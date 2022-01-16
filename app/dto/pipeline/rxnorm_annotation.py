from app.dto.base_dto import BaseDto
from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class RxNormAnnotation(BaseDto, BasePipelineComponentResult):
    code: str
    description: str
    score: float
