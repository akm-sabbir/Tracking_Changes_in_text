import re
from typing import Dict, List

import spacy
from spacy.tokens import Token

from app.dto.core.service.Tokens import TokenInfo
from app.service.icd10_negation_service import ICD10NegationService
from app.service.impl.icd10_negation_service_impl import Icd10NegationServiceImpl
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.icd10_tokenizing_text_component import TextTokenizationComponent
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.service.pipeline.components.icd10_tokenizing_text_component import TextTokenizationComponent
from app.settings import Settings
from app.util.dependency_injector import DependencyInjector
from app.util.pipeline_util import PipelineUtil
from app.dto.pipeline.negation_component_result import NegationResult


class NegationHandlingComponent(BasePipelineComponent):
    DEPENDS_ON = [SubjectiveSectionExtractorComponent, MedicationSectionExtractorComponent, TextTokenizationComponent]

    def __init__(self):
        super().__init__()
        self.__icd10_negation_fixing_service: ICD10NegationService = DependencyInjector.get_instance(
            Icd10NegationServiceImpl)

    def run(self, annotation_results: dict) -> List[NegationResult]:
        if annotation_results['acm_cached_result'] is not None:
            return []
        tokenizer = Settings.get_settings_tokenizer()

        subjective_section_text_tokens = self.__fix_negation_for_section(
                                                                         annotation_results[
                                                                            TextTokenizationComponent][
                                                                            0].token_container,
                                                                         annotation_results)

        medication_section_text_tokens = self.__fix_negation_for_section(
                                                                         annotation_results[
                                                                            TextTokenizationComponent][
                                                                            1].token_container,
                                                                         annotation_results)
        subjective_section_text = "".join(subjective_section_text_tokens).strip()
        medication_section_text = "".join(medication_section_text_tokens).strip()

        return [NegationResult(text=subjective_section_text),
                NegationResult(text=medication_section_text)]

    def __fix_negation_for_section(self, token_container: List[TokenInfo], annotation_results: dict):

        for index, token in enumerate(token_container):
            each_token = token.token.lower()
            if each_token.lower().find("no") == 0:
                fixed_token = self.__icd10_negation_fixing_service.get_icd_10_text_negation_fixed(each_token)
                text_tokens[index] = fixed_token
                self._track_text_change(fixed_token, each_token, token, annotation_results)

        return (" " + each_token if each_token not in [",", "?", "!", ".", ";", ":"] else each_token
                for each_token in text_tokens)

    def _track_text_change(self, fixed_token: str, each_token: str, token: Token, annotation_results: Dict):
        fixed_words = re.sub(r"[^\w]", " ", fixed_token).split()
        if len(fixed_words) < 2:
            return
        original_word = each_token.replace("no", "").strip()
        changed_word = fixed_words[1]
        start = token.idx + each_token.find(original_word)
        end = token.idx + len(original_word)
        PipelineUtil.track_changed_words(original_word, changed_word, start, end, annotation_results)
