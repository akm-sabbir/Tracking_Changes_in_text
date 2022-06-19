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

        for index, section in enumerate(subjective_section_matches):
            relative_start = current_section_relative_start
            relative_end = current_section_relative_start + len(section.group())
            text = section.group()
            if section.group()[-1] not in set(['.', ',', ';']):
                text = self.__get_modified_text(text, index, subjective_section_matches, '.')
                relative_end = relative_end + (2 if index != len(subjective_section_matches) - 1 else 1)
            else:
                text += self.__get_modified_text(text, index, subjective_section_matches, '')
                relative_end = relative_end + (1 if index != len(subjective_section_matches) - 1 else 0)

            current_section = SubjectiveSection(text, section.start(), section.end(), relative_start,
                                                relative_end)
            current_section_relative_start = current_section.relative_end
            subjective_sections.append(current_section)

        subjective_text = "".join([section.text for section in subjective_sections])

        if subjective_text == "":
            subjective_text = annotation_results["text"]
            subjective_sections.append(SubjectiveSection(subjective_text, 0, len(subjective_text), 0,
                                                         len(subjective_text)))

        return [SubjectiveText(subjective_text, subjective_sections)]

    def __get_modified_text(self, source_text: str, index: int, subjective_section_matches: List, modifier: str):
        if index != len(subjective_section_matches) - 1:
            return source_text + f"{modifier} "
        else:
            return source_text + f"{modifier}"
