from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class ChangedWordAnnotation(BasePipelineComponentResult):
    def __init__(self, changed_text: str, original_text: str, start: int, end: int):
        self.changed_text: str = changed_text
        self.original_text: str = original_text
        self.start: int = start
        self.end: int = end
