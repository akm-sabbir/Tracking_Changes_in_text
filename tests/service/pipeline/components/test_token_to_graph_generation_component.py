import time
from unittest import TestCase

from app.dto.core.trie_structure import Trie
from app.dto.pipeline.medication_section import MedicationText
from app.dto.pipeline.subjective_section import SubjectiveText
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.service.pipeline.components.icd10_token_to_graph_generation_component import TextToGraphGenerationComponent
from app.service.pipeline.components.icd10_tokenizing_text_component import TextTokenizationComponent
from app.dto.pipeline import token_graph_component
from app.dto.core.service.Tokens import TokenInfo


class TestTokenToGraphGenerationComponent(TestCase):

    def test__run__should_return_correct_response__given_correct_input(self, ):
        graph_generation_component = TextToGraphGenerationComponent()

        test_text_set_one = "He has alot going on, he continues to drinks, daily, " \
                            "and he has been feeling dizzy with some fall,he was in the er recently " \
                            "and he had a head CT, he still smokes, coughing wheezying breathless, withsputum, " \
                            "he stil has urinary incontinent, he has been confirmed to have colon cancer, " \
                            "he am not sure he has hallucinations, he not sleeping well, he has chronic urinary and bowel incontinent, " \
                            "he also chronic"
        test_text_span_set_one_subjective_section = [TokenInfo(token="He", start_of_span=0, end_of_span=2, offset=0),
                                                     TokenInfo(token="has", start_of_span=3, end_of_span=6, offset=0),
                                                     TokenInfo(token="alot", start_of_span=7, end_of_span=11, offset=0),
                                                     TokenInfo(token="going", start_of_span=12, end_of_span=17,
                                                               offset=0),
                                                     TokenInfo(token="on", start_of_span=18, end_of_span=20, offset=0),
                                                     TokenInfo(token=",", start_of_span=20, end_of_span=21, offset=0),
                                                     TokenInfo(token="he", start_of_span=22, end_of_span=24, offset=0)]
        test_text_span_set_one_medication_section = [
            TokenInfo(token="continues", start_of_span=25, end_of_span=34, offset=0),
            TokenInfo(token="to", start_of_span=35, end_of_span=37, offset=0),
            TokenInfo(token="drinks", start_of_span=38, end_of_span=44, offset=0)]
        set_one_graph_generation_result = graph_generation_component.run({"text": test_text_set_one,
                                                                          "acm_cached_result": None,
                                                                          "changed_words": {},
                                                                          TextTokenizationComponent: [
                                                                              test_text_span_set_one_subjective_section,
                                                                              test_text_span_set_one_medication_section],
                                                                          SubjectiveSectionExtractorComponent: [
                                                                              SubjectiveText(test_text_set_one, [])],
                                                                          MedicationSectionExtractorComponent: [
                                                                              MedicationText(test_text_set_one, [])],
                                                                          })
        assert set_one_graph_generation_result[0].graph_token_container['He'][0].pos_tracking == 0
        assert set_one_graph_generation_result[0].graph_token_container['on'][18].pos_tracking == 18
        assert set_one_graph_generation_result[1].graph_token_container['he'][22].pos_tracking == 22
        assert set_one_graph_generation_result[1].graph_token_container['he'][22].is_root is True
        assert set_one_graph_generation_result[1].graph_token_container['he'][22].parent_token == ""
        assert set_one_graph_generation_result[1].graph_token_container.get(",", None) is None
