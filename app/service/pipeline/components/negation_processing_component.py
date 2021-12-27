import re
from typing import Dict

from spacy.tokens import Token

from app.service.icd10_negation_service import ICD10NegationService
from app.service.impl.icd10_negation_service_impl import Icd10NegationServiceImpl
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.settings import Settings
from app.util.dependency_injector import DependencyInjector
from app.util.pipeline_util import PipelineUtil


class NegationHandlingComponent(BasePipelineComponent):
    DEPENDS_ON = [SubjectiveSectionExtractorComponent]

    def __init__(self):
        super().__init__()
        self.__icd10_negation_fixing_service: ICD10NegationService = DependencyInjector.get_instance(
            Icd10NegationServiceImpl)

    def run(self, annotation_results: dict) -> list:
        if annotation_results['acm_cached_result'] is not None:
            return []
        tokenize = Settings.get_settings_tokenizer()
        text = annotation_results[SubjectiveSectionExtractorComponent][0].text
        tokens = tokenize(text.lower())
        text_tokens = [each.text for each in tokens]
        for index, token in enumerate(tokens):
            each_token = token.text.lower()
            if each_token.lower().find("no") == 0:
                fixed_token = self.__icd10_negation_fixing_service.get_icd_10_text_negation_fixed(each_token)
                text_tokens[index] = fixed_token
                self._track_text_change(fixed_token, each_token, token, annotation_results)

        text_tokens = [" " + each_token if each_token not in [",", "?", "!", ".", ";", ":"] else each_token
                       for each_token in text_tokens]
        return ["".join(text_tokens).strip()]

    def _track_text_change(self, fixed_token: str, each_token: str, token: Token, annotation_results: Dict):
        fixed_words = re.sub(r"[^\w]", " ", fixed_token).split()
        if len(fixed_words) < 2:
            return
        original_word = each_token.replace("no", "").strip()
        changed_word = fixed_words[1]
        start = token.idx + each_token.find(original_word)
        end = token.idx + len(original_word)
        PipelineUtil.track_changed_words(original_word, changed_word, start, end, annotation_results)
