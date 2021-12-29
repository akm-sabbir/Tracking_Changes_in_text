from typing import List

from app.dto.pipeline.subjective_section import SubjectiveSection, SubjectiveText
from app.service.medeant.medant_note_section_service import MedantNoteSectionService
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.util.dependency_injector import DependencyInjector


class SubjectiveSectionExtractorComponent(BasePipelineComponent):
    DEPENDS_ON = []
    note_section_service: MedantNoteSectionService = DependencyInjector.get_instance(MedantNoteSectionService)
    section_separator = "\n\n------------------------------------------------------\n\n"

    def run(self, annotation_results: dict) -> List[SubjectiveText]:
        subjective_section_matches = self.note_section_service.get_subjective_sections(
            annotation_results["text"])

        subjective_sections = []
        current_section_relative_start = 0

        for section in subjective_section_matches:
            relative_start = current_section_relative_start
            relative_end = current_section_relative_start + len(section.group())
            current_section = SubjectiveSection(section.group(), section.start(), section.end(), relative_start,
                                                relative_end)
            current_section_relative_start = current_section.relative_end + len(self.section_separator)
            subjective_sections.append(current_section)

        subjective_text = self.section_separator.join([section.text for section in subjective_sections])

        if subjective_text == "":
            subjective_text = annotation_results["text"]
            subjective_sections.append(SubjectiveSection(subjective_text, 0, len(subjective_text), 0,
                                                         len(subjective_text)))

        return [SubjectiveText(subjective_text, subjective_sections)]
