import re
from typing import Dict, List

import spacy
from app.dto.core.service.Tokens import TokenInfo
from app.service.icd10_negation_service import ICD10NegationService
from app.service.impl.icd10_text_token_span_gen_service_impl import ICD10TextAndSpanGenerationServiceImpl
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.settings import Settings
from app.util.dependency_injector import DependencyInjector
from app.dto.pipeline.tokenization_component_result import TokenizationResult


class TextTokenizationComponent(BasePipelineComponent):
    DEPENDS_ON = [SubjectiveSectionExtractorComponent, MedicationSectionExtractorComponent]

    def __init__(self):
        super().__init__()
        self.__icd10_text_tokenizing_and_span_generation_service: ICD10TextAndSpanGenerationServiceImpl\
            = DependencyInjector.get_instance(
            ICD10TextAndSpanGenerationServiceImpl)

    def run(self, annotation_results: dict) -> List[TokenizationResult]:
        if annotation_results['acm_cached_result'] is not None:
            return []

        subjective_section_text_tokens_and_span: List[TokenInfo] = \
            self.__icd10_text_tokenizing_and_span_generation_service.get_token_with_span(
                                                                         annotation_results[
                                                                            SubjectiveSectionExtractorComponent][
                                                                            0].text)

        medication_section_text_tokens_and_span = \
            self.__icd10_text_tokenizing_and_span_generation_service.get_token_with_span(
                                                                         annotation_results[
                                                                            MedicationSectionExtractorComponent][
                                                                            0].text)

        return [TokenizationResult(complex_container=subjective_section_text_tokens_and_span),
                TokenizationResult(complex_container=medication_section_text_tokens_and_span)]