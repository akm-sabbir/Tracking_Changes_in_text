from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class TokenizationResult(BasePipelineComponentResult):
    def __init__(self, complex_container: list):
        self.token_container: list = complex_container
