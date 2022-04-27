from typing import Dict, List

from app.dto.core.service.Tokens import TokenInfo
from app.service.icd10_negation_service import ICD10NegationService
from app.service.impl.icd10_negation_service_impl import Icd10NegationServiceImpl
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.service.pipeline.components.icd10_tokenizing_text_component import TextTokenizationComponent
from app.settings import Settings
from app.util.dependency_injector import DependencyInjector
from app.util.pipeline_util import PipelineUtil
from app.dto.pipeline.negation_component_result import NegationResult
from app.util.text_span_discovery import TextSpanDiscovery
from app.service.pipeline.components.icd10_token_to_graph_generation_component import GraphTokenResult


class NegationHandlingComponent(BasePipelineComponent):
    DEPENDS_ON = [SubjectiveSectionExtractorComponent, MedicationSectionExtractorComponent, TextTokenizationComponent]

    def __init__(self):
        super().__init__()
        self.__icd10_negation_fixing_service: ICD10NegationService = DependencyInjector.get_instance(
            Icd10NegationServiceImpl)
        self.__text_span_discovery: TextSpanDiscovery = TextSpanDiscovery()

    def run(self, annotation_results: dict) -> List[NegationResult]:
        if annotation_results['acm_cached_result'] is not None:
            return []
        tokenizer = Settings.get_settings_tokenizer()

        updated_graph, new_subjective_section_text_tokens = self.__fix_negation_for_section(
                                                                         annotation_results[
                                                                            TextTokenizationComponent][
                                                                            0].token_container,
                                                                         annotation_results[GraphTokenResult][0])
        annotation_results[GraphTokenResult][0] = updated_graph
        updated_graph, new_medication_section_text_tokens = self.__fix_negation_for_section(
                                                                         annotation_results[
                                                                            TextTokenizationComponent][
                                                                            1].token_container,
                                                                         annotation_results[GraphTokenResult][1])
        annotation_results[GraphTokenResult][1] = updated_graph

        return [NegationResult(token_info_with_span=new_subjective_section_text_tokens),
                NegationResult(token_info_with_span=new_medication_section_text_tokens)]

    def __fix_negation_for_section(self, token_container: List[TokenInfo], token_graphs: dict):
        changed_token_dict = {}
        for index, token in enumerate(token_container):
            each_token = token.token.lower()
            token_container[index].token = each_token
            if each_token.find("no") == 0:
                fixed_token = self.__icd10_negation_fixing_service.get_icd_10_text_negation_fixed(each_token)
                changed_token_dict[each_token] = fixed_token
        updated_graphs, new_text_span = self._track_text_change_part(changed_token_dict, token_container, token_graphs)

        return

    def _track_text_change_part(self,dictionary: dict, token_container: List[TokenInfo], token_graphs):
        self.__text_span_discovery.set_changed_text_dictionary(dictionary)
        updated_graphs, new_text_span = self.__text_span_discovery.generate_metainfo_for_changed_text(token_graphs, token_container)
        return updated_graphs, new_text_span