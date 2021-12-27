from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.settings import Settings
from app.service.icd10_negation_service import ICD10NegationService
from app.service.impl.icd10_negation_service_impl import Icd10NegationServiceImpl
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.util.dependency_injector import DependencyInjector


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
        for index, each_token in enumerate(text_tokens):
            if each_token.lower().find("no") == 0:
                text_tokens[index] = self.__icd10_negation_fixing_service.get_icd_10_text_negation_fixed(each_token)
        text_tokens = [" " + each_token if each_token not in [",", "?", "!", ".", ";", ":"] else each_token
                       for each_token in text_tokens]
        return ["".join(text_tokens).strip()]