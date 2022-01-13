from app.dto.base_dto import BaseDto
from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class RxNormAttributeAnnotation(BaseDto, BasePipelineComponentResult):
    score: float
    attribute_type: str
    relationship_score: float
    id: int
    begin_offset: int
    end_offset: int
    text: str
