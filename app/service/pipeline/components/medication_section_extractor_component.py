from typing import List

from app.dto.pipeline.medication_section import MedicationSection, MedicationText
from app.service.medeant.medant_note_section_service import MedantNoteSectionService
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.util.dependency_injector import DependencyInjector


def get_modified_text(source_text: str, modifier: str):
    return source_text + modifier


class MedicationSectionExtractorComponent(BasePipelineComponent):
    DEPENDS_ON = []
    note_section_service: MedantNoteSectionService = DependencyInjector.get_instance(MedantNoteSectionService)

    def run(self, annotation_results: dict) -> List[MedicationText]:
        medication_section_matches = self.note_section_service.get_medication_sections(
            annotation_results["text"])

        medication_sections = []
        current_section_relative_start = 0

        for index, section in enumerate(medication_section_matches):
            relative_start = current_section_relative_start
            relative_end = current_section_relative_start + len(section.group())
            text = section.group()
            if section.group()[-1] not in set(['.', ',', ';']):
                text = get_modified_text(text, '. ' if index != len(medication_section_matches) - 1 else '.')
                relative_end = relative_end + (2 if index != len(medication_section_matches) - 1 else 1)
            else:
                text = get_modified_text(text, ' ' if index != len(medication_section_matches) - 1 else '')
                relative_end = relative_end + (1 if index != len(medication_section_matches) - 1 else 0)

            current_section = MedicationSection(text, section.start(), section.end(), relative_start,
                                                relative_end)
            current_section_relative_start = current_section.relative_end
            medication_sections.append(current_section)

        medication_text = "".join([section.text for section in medication_sections])

        if medication_text == "":
            medication_text = annotation_results["text"]
            medication_sections.append(MedicationSection(medication_text, 0, len(medication_text), 0,
                                                         len(medication_text)))

        return [MedicationText(medication_text, medication_sections)]

