from typing import List

from app.dto.pipeline.subjective_section import SubjectiveSection, SubjectiveText
from app.service.medeant.medant_note_section_service import MedantNoteSectionService
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.util.dependency_injector import DependencyInjector
from app.service.pipeline.components.icd10_smoking_pattern_detection import PatientSmokingConditionDetectionComponent
from app.service.pipeline.components.section_exclusion_service_component import SectionExclusionServiceComponent


class SubjectiveSectionExtractorComponent(BasePipelineComponent):
    DEPENDS_ON = [PatientSmokingConditionDetectionComponent, SectionExclusionServiceComponent]
    note_section_service: MedantNoteSectionService = DependencyInjector.get_instance(MedantNoteSectionService)

    def run(self, annotation_results: dict) -> List[SubjectiveText]:
        subjective_section_matches = self.note_section_service.get_subjective_sections(
            annotation_results["text"])

        subjective_sections = []
        current_section_relative_start = 0

        for section in subjective_section_matches:
            relative_start = current_section_relative_start
            section_text = section.group().replace("\n", " ").rstrip() + ".\n"
            relative_end = current_section_relative_start + len(section_text)

            current_section = SubjectiveSection(section_text, section.start(),
                                                section.start() +
                                                len(section_text),
                                                relative_start,
                                                relative_end)

            current_section_relative_start = current_section.relative_end
            subjective_sections.append(current_section)

        subjective_text = "".join([section.text for section in subjective_sections])

        if subjective_text == "":
            subjective_text = annotation_results["text"]
            subjective_sections.append(SubjectiveSection(subjective_text, 0, len(subjective_text), 0,
                                                         len(subjective_text)))

        return [SubjectiveText(subjective_text, subjective_sections)]
