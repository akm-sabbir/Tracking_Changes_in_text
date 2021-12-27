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

        subjective_sections = [SubjectiveSection(section.group(), section.start(), section.end()) for section in
                               subjective_section_matches]

        subjective_text = self.section_separator.join([section.text for section in subjective_sections])

        return [SubjectiveText(subjective_text, subjective_sections)]
