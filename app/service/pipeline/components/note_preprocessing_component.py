from typing import List

from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.pipeline.medication_section import MedicationText
from app.dto.pipeline.negation_component_result import NegationResult
from app.dto.pipeline.subjective_section import SubjectiveText
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.icd10_text_reconstruction_component import TextReconstructionComponent
from app.service.pipeline.components.icd10_token_to_graph_generation_component import TextTokenizationComponent
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.util.config_manager import ConfigManager
from app.util.encounter_note_util import EncounterNoteUtil


class NotePreprocessingComponent(BasePipelineComponent):
    DEPENDS_ON = [SubjectiveSectionExtractorComponent, MedicationSectionExtractorComponent, TextTokenizationComponent,
                  NegationHandlingComponent]

    def reconstruct_text(self, span_information: NegationResult):
        array_size = span_information.tokens_with_span[-1].start_of_span
        text_container = [" "]*(array_size + 1)
        for each_tuple in span_information.tokens_with_span:
            text_container[each_tuple.start_of_span:len(each_tuple.token)] = each_tuple.token[:]
        return "".join(text_container)

    def run(self, annotation_results: dict) -> List[Paragraph]:
        if annotation_results['acm_cached_result'] is not None:
            return []
        subjective_section_text_span: NegationResult = annotation_results[NegationHandlingComponent][0]
        medication_section_text_span: NegationResult = annotation_results[NegationHandlingComponent][1]
        subjective_section_text = self.reconstruct_text(subjective_section_text_span)
        medication_section_text = self.reconstruct_text(medication_section_text_span)

        return [EncounterNoteUtil.break_note_into_paragraphs(subjective_section_text.text,
                                                             int(ConfigManager.get_specific_config("acm",
                                                                                                   "char_limit"))),
                EncounterNoteUtil.break_note_into_paragraphs(medication_section_text.text,
                                                             int(ConfigManager.get_specific_config("acm",
                                                                                                   "char_limit")))
                ]
