from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class NegationResult(BasePipelineComponentResult):
    def __init__(self, text: str):
        self.text: str = text
