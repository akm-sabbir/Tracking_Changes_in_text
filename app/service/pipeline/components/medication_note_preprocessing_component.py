from typing import List

from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.pipeline.medication_section import MedicationText
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.util.config_manager import ConfigManager
from app.util.encounter_note_util import EncounterNoteUtil


class MedicationNotePreprocessingComponent(BasePipelineComponent):
    DEPENDS_ON = []

    def run(self, annotation_results: dict) -> List[Paragraph]:
        if annotation_results['acm_cached_result'] is not None:
            return []
        text: MedicationText = annotation_results[MedicationSectionExtractorComponent][0]
        return EncounterNoteUtil.break_note_into_paragraphs(text.text,
                                                            int(ConfigManager.get_specific_config("acm", "char_limit")))
