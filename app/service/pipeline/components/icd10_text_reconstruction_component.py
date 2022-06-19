from typing import List

from app.dto.pipeline.medication_section import MedicationText
from app.dto.pipeline.negation_component_result import NegationResult
from app.dto.pipeline.subjective_section import SubjectiveText
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.icd10_token_to_graph_generation_component import TextTokenizationComponent
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent


class TextReconstructionComponent(BasePipelineComponent):
    DEPENDS_ON = [SubjectiveSectionExtractorComponent, MedicationSectionExtractorComponent, TextTokenizationComponent,
                  TextTokenizationComponent, NegationHandlingComponent]

    def reconstruct_text(self, span_information: NegationResult):
        array_size = span_information.tokens_with_span[-1].end_of_span
        text_container = [" "] * array_size

        for each_tuple in span_information.tokens_with_span:
            text_container[each_tuple.start_of_span:each_tuple.start_of_span + len(each_tuple.token)] = each_tuple.token

        return "".join(text_container)

    def run(self, annotation_results: dict) -> List:
        if annotation_results['acm_cached_result'] is not None:
            return []
        subjective_section_text_span: NegationResult = annotation_results[NegationHandlingComponent][0]
        medication_section_text_span: NegationResult = annotation_results[NegationHandlingComponent][1]
        subjective_section_text = self.reconstruct_text(subjective_section_text_span)
        medication_section_text = self.reconstruct_text(medication_section_text_span)
        return [SubjectiveText(subjective_section_text,
                               annotation_results[SubjectiveSectionExtractorComponent][0].subjective_sections),
                MedicationText(medication_section_text,
                               annotation_results[MedicationSectionExtractorComponent][0].medication_sections)]
