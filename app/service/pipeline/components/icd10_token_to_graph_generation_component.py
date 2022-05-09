import re
from typing import Dict, List

import spacy
from app.dto.core.service.Tokens import TokenInfo
from app.service.icd10_negation_service import ICD10NegationService
from app.service.impl.icd10_text_token_span_gen_service_impl import ICD10TextAndSpanGenerationServiceImpl
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.util.dependency_injector import DependencyInjector
from app.dto.pipeline.token_graph_component import GraphTokenResult
from app.service.impl.icd10_generate_graph_from_text_impl import ICD10GenerateGraphFromTextImpl
from app.service.pipeline.components.icd10_tokenizing_text_component import TextTokenizationComponent


class TextToGraphGenerationComponent(BasePipelineComponent):
    DEPENDS_ON = [SubjectiveSectionExtractorComponent, MedicationSectionExtractorComponent, TextTokenizationComponent
                  ]

    def __init__(self):
        super().__init__()
        self.__icd10_text_to_graph_generation_service: ICD10GenerateGraphFromTextImpl\
            = DependencyInjector.get_instance(
            ICD10GenerateGraphFromTextImpl)

    def run(self, annotation_results: dict) -> dict:
        if annotation_results['acm_cached_result'] is not None:
            return []

        subjective_section_text_tokens_graph: List[TokenInfo] = \
            self.__icd10_text_to_graph_generation_service.process_token_to_create_graph(
                                                                         annotation_results[TextTokenizationComponent][
                                                                            0])

        medication_section_text_tokens_graph = \
            self.__icd10_text_to_graph_generation_service.process_token_to_create_graph(
                                                                         annotation_results[TextTokenizationComponent][1])

        return [GraphTokenResult(graph_container=subjective_section_text_tokens_graph),
                GraphTokenResult(graph_container=medication_section_text_tokens_graph)]