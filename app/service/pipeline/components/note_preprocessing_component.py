from typing import List

from app.dto.core.paragraph import Paragraph
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.util.config_manager import ConfigManager
from app.util.encounter_note_util import EncounterNoteUtil


class NotePreprocessingComponent(BasePipelineComponent):
    DEPENDS_ON = []

    def run(self, annotation_results: dict) -> List[Paragraph]:
        text = annotation_results['text']
        return EncounterNoteUtil.break_note_into_paragraphs(text,
                                                            int(ConfigManager.get_specific_config("acm", "char_limit")))
