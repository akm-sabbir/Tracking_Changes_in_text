from unittest import TestCase
from app.dto.core.trie_structure import Trie
from app.dto.pipeline.medication_section import MedicationText
from app.dto.pipeline.negation_component_result import NegationResult
from app.dto.pipeline.subjective_section import SubjectiveText
from app.dto.pipeline.token_graph_component import GraphTokenResult
from app.dto.pipeline.tokenization_component_result import TokenizationResult
from app.service.impl.icd10_generate_graph_from_text_impl import ICD10GenerateGraphFromTextImpl
from app.service.pipeline.components.icd10_tokenizing_text_component import TextTokenizationComponent
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.service.pipeline.components.icd10_token_to_graph_generation_component import TextToGraphGenerationComponent
from app.dto.core.service.Tokens import TokenInfo
from app.dto.core.util.TokenNode import TokenNode
from app.service.pipeline.components.icd10_text_reconstruction_component import TextReconstructionComponent


class TestTextReconstructionComponent(TestCase):

    def get_new_node_for_token(self, parent_key: str = "", is_root=True, pos_list: list = [], length: int = 0):
        new_node = TokenNode()
        new_node.pos_tracking = ICD10GenerateGraphFromTextImpl.ROOT_LOCATION
        new_node.pos_list = pos_list
        new_node.is_root = is_root
        new_node.length = length
        new_node.parent_token = parent_key
        return new_node

    def test__run__should_return_correct_response__given_correct_input(self, ):
        text_reconstruction_component = TextReconstructionComponent()
        test_text_span_set_one_subjective_section = [
            TokenInfo(token="He", start_of_span=0, end_of_span=2, offset=0),
            TokenInfo(token="has", start_of_span=3, end_of_span=6, offset=0),
            TokenInfo(token="alot", start_of_span=7, end_of_span=11, offset=0),
            TokenInfo(token="going", start_of_span=12, end_of_span=17, offset=0),
            TokenInfo(token="on", start_of_span=18, end_of_span=20, offset=0),
            TokenInfo(token=",", start_of_span=20, end_of_span=21, offset=0),
            TokenInfo(token="he", start_of_span=22, end_of_span=24, offset=0)]
        test_text_span_set_one_medication_section = [
            TokenInfo(token="continues", start_of_span=25, end_of_span=34, offset=0),
            TokenInfo(token="to", start_of_span=35, end_of_span=37, offset=0),
            TokenInfo(token="drinks", start_of_span=38, end_of_span=44, offset=0),
            TokenInfo(token="daily", start_of_span=46, end_of_span=51, offset=0),
            TokenInfo(token="nopain", start_of_span=52, end_of_span=58, offset=0),
            TokenInfo(token="nobreathlessness", start_of_span=59, end_of_span=75, offset=0)
            ]
        test_text_set_one = "He has alot going on, he continues to drinks, daily, nopain, nobreathlessness, " \
                            "and he has been feeling dizzy with some fall,he was in the er recently " \
                            "and he had a head CT, he still smokes, coughing wheezying breathless, withsputum, " \
                            "he stil has urinary incontinent, he has been confirmed to have colon cancer, " \
                            "he am not sure he has hallucinations, he not sleeping well, he has chronic urinary and bowel incontinent, " \
                            "he also chronic"
        dict_for_subjective_section = {}
        dict_for_medication_section = {}
        dict_for_subjective_section["has"] = {}
        dict_for_subjective_section["has"][3] = self.get_new_node_for_token(length=len("has"))
        dict_for_medication_section["nopain"] = {}
        dict_for_medication_section["nopain"][46] = self.get_new_node_for_token(length=len("nopain"))
        dict_for_medication_section["nobreathlessness"] = {}
        dict_for_medication_section["nobreathlessness"][54] = self.get_new_node_for_token(
            length=len("nobreathlessness"))
        results = text_reconstruction_component.run({"text": test_text_set_one,
                                        "acm_cached_result": None, "changed_words": {},
                                        TextTokenizationComponent: [TokenizationResult(complex_container=test_text_span_set_one_subjective_section),
                                                                    TokenizationResult(complex_container=test_text_span_set_one_medication_section)],
                                        TextToGraphGenerationComponent: [GraphTokenResult(graph_container=dict_for_subjective_section),
                                                                         GraphTokenResult(graph_container=dict_for_medication_section)],
                                        SubjectiveSectionExtractorComponent: [SubjectiveText(test_text_set_one, [])],
                                        MedicationSectionExtractorComponent: [MedicationText(test_text_set_one, [])],
                                        NegationHandlingComponent: [NegationResult(token_info_with_span=test_text_span_set_one_subjective_section),
                NegationResult(token_info_with_span=test_text_span_set_one_medication_section)]})
        print(results[1].text + " " + str(len(results[1].text)))
        print(results[0].text + " " + str(len(results[0].text)))
        assert results[1].text[52:58] =='nopain'
        assert results[1].text[59:75] =='nobreathlessness'

    def test__run__should_return_empty__given_cache_present(self):
        component = TextReconstructionComponent()
        result = component.run({"text": "some text.\n\nSome other text", 'acm_cached_result': ["some data"]})
        assert result == []