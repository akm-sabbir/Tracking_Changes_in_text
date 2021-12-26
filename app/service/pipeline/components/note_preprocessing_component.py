from typing import List
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.util.config_manager import ConfigManager
from app.util.encounter_note_util import EncounterNoteUtil
from app.dto.pipeline.negation_component_result import NegationResult


class NotePreprocessingComponent(BasePipelineComponent):
    DEPENDS_ON = [NegationHandlingComponent]

    def run(self, annotation_results: dict) -> List[BasePipelineComponent]:
        if annotation_results['acm_cached_result'] is not None:
            return []
        text: NegationResult = annotation_results[NegationHandlingComponent][0]
        return EncounterNoteUtil.break_note_into_paragraphs(text.text,
                                                            int(ConfigManager.get_specific_config("acm", "char_limit")))
