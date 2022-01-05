from typing import List

from app.dto.pipeline.excluded_sections.family_history_excluded_section import FamilyHistorySection
from app.service.medeant.medant_note_section_service import MedantNoteSectionService
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.util.dependency_injector import DependencyInjector


class SectionExclusionServiceComponent(BasePipelineComponent):
    DEPENDS_ON = []
    note_section_service: MedantNoteSectionService = DependencyInjector.get_instance(MedantNoteSectionService)

    def run(self, annotation_results: dict) -> List[FamilyHistorySection]:
        # list of exclusion service components will be here...
        
        fh_excluded_sections = self.note_section_service.get_family_history_sections(
            annotation_results["text"]
        )

        return fh_excluded_sections
