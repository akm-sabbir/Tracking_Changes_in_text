from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class Paragraph(BasePipelineComponentResult):

    def __init__(self, text, start_index, end_index, relative_position):
        self.text = text
        self.start_index = start_index
        self.end_index = end_index
        self.relative_position = relative_position

    text: str
    start_index: int
    end_index: int
    relative_position: int
