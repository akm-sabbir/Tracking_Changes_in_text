from typing import List

from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class MedicationSection(BasePipelineComponentResult):
    def __init__(self, text: str, start: int, end: int, relative_start: int, relative_end: int):
        self.text = text
        self.start = start
        self.end = end
        self.relative_start = relative_start
        self.relative_end = relative_end


class MedicationText(BasePipelineComponentResult):
    def __init__(self, text: str, medication_sections: List[MedicationSection]):
        self.text = text
        self.medication_sections = medication_sections
