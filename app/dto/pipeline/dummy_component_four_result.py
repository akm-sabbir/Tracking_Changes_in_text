from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class DummyComponentFourResult(BasePipelineComponentResult):
    def __init__(self, message: str):
        self.message = message
