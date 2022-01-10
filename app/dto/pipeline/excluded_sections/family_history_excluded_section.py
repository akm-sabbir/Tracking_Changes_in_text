from app.dto.pipeline.excluded_sections.excluded_section import ExcludedSection


class FamilyHistorySection(ExcludedSection):
    def __init__(self, start: int, end: int):
        super().__init__(start, end)
