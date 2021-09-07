from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class DummyComponentThreeResult(BasePipelineComponentResult):
    def __init__(self, message: str):
        self.message = message
