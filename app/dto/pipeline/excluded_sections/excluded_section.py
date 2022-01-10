from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class ExcludedSection(BasePipelineComponentResult):
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        