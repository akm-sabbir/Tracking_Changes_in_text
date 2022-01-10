from typing import List

from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult
from app.dto.pipeline.medication_section import MedicationSection, MedicationText
from app.service.medeant.medant_note_section_service import MedantNoteSectionService
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.util.dependency_injector import DependencyInjector


class MedicationSectionExtractorComponent(BasePipelineComponent):
    DEPENDS_ON = []
    note_section_service: MedantNoteSectionService = DependencyInjector.get_instance(MedantNoteSectionService)

    def run(self, annotation_results: dict) -> List[MedicationText]:
        medication_section_matches = self.note_section_service.get_medication_sections(
            annotation_results["text"])

        medication_sections = []
        current_section_relative_start = 0

        for section in medication_section_matches:
            relative_start = current_section_relative_start
            relative_end = current_section_relative_start + len(section.group())
            current_section = MedicationSection(section.group(), section.start(), section.end(), relative_start,
                                                relative_end)
            current_section_relative_start = current_section.relative_end
            medication_sections.append(current_section)

        medication_text = "".join([section.text for section in medication_sections])

        if medication_text == "":
            medication_text = annotation_results["text"]
            medication_sections.append(MedicationSection(medication_text, 0, len(medication_text), 0,
                                                         len(medication_text)))

        print(medication_text)

        return [MedicationText(medication_text, medication_sections)]

