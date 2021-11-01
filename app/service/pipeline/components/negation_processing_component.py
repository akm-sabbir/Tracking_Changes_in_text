
from collections import defaultdict
from typing import List

from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.impl.icd10_negation_service_impl import Icd10NegationServiceImpl
from app.util.dependency_injector import DependencyInjector
from app.service.icd10_negation_service import ICD10NegationService
from app.Settings import Settings


class NegationHandlingComponent(BasePipelineComponent):

    DEPENDS_ON = []

    def __init__(self):
        super().__init__()
        self.__icd10_negation_fixing_service: ICD10NegationService = DependencyInjector.get_instance(
            Icd10NegationServiceImpl)

    def run(self, annotation_results: dict) -> str:
        if annotation_results['acm_cached_result'] is not None:
            return []
        tokenize = Settings.get_settings_tokenizer()
        text = annotation_results['text']
        tokens = tokenize(text.lower())
        text_tokens = [each.text for each in tokens]
        for index, each_token in enumerate(text_tokens):
            if each_token.lower().find("no") == 0:
                text_tokens[index] = self.__icd10_negation_fixing_service.get_icd_10_text_negation_fixed(each_token)
        return " ".join(text_tokens)