from unittest import TestCase
from unittest.mock import patch, Mock
from app.service.impl.icd10_generate_graph_from_text_impl import ICD10GenerateGraphFromTextImpl
from app.service.impl.icd10_text_token_span_gen_service_impl import ICD10TextAndSpanGenerationServiceImpl


class TestICD10GenerateGraphFromTextServiceImplTest(TestCase):
    icd10TextTokenGenerator: ICD10TextAndSpanGenerationServiceImpl
    icd10TextGraphGenerator: ICD10GenerateGraphFromTextImpl

    def test_graph_dict_from_token_should_return_proper_datastructure(self) -> None:
        self.icd10TextTokenGenerator = ICD10TextAndSpanGenerationServiceImpl()
        self.icd10TextGraphGenerator = ICD10GenerateGraphFromTextImpl()
        test_text1 = "as the patient queried about smoking behavior? Yes No\n" \
                     "Does the patient currently smoke? Smoking: Patient has never smoked - (1/21/2020).\n"
        test_result1 = self.icd10TextTokenGenerator.get_token_with_span(test_text1)
        actual_test_result1 = self.icd10TextTokenGenerator.process_each_token(test_result1)
        graph_nodes = self.icd10TextGraphGenerator.process_token_to_create_graph(actual_test_result1)
        assert graph_nodes['patient'][7].pos_tracking[7] == 7
        assert graph_nodes['patient'][63].pos_tracking[63] == 63
        assert graph_nodes['patient'][63].length == 7
        assert graph_nodes['patient'][7].length == 7
        assert graph_nodes['patient'][7].parent_token == ""
        assert graph_nodes['patient'][63].parent_token == ""
        assert graph_nodes.get("?", None) == None
        assert graph_nodes['patient'][7].is_root == True

    def test_graph_dict_from_token_should_return_proper_datastructure_second_set(self) -> None:
        self.icd10TextTokenGenerator = ICD10TextAndSpanGenerationServiceImpl()
        self.icd10TextGraphGenerator = ICD10GenerateGraphFromTextImpl()
        test_text1 = "He has alot going on, he continues to drinks, daily, " \
                     "and he has been feeling dizzy with some fall,he was in the er recently " \
                     "and he had a head CT, he still smokes, coughing wheezying breathless, withsputum, " \
                     "he stil has urinary incontinent, he has been confirmed to have colon cancer, " \
                     "he am not sure he has hallucinations, he not sleeping well, he has chronic urinary and bowel incontinent, " \
                     "he also chronic diarrheafrom time to time,  the absence of recurrent leg cramps is obvious"
        test_result1 = self.icd10TextTokenGenerator.get_token_with_span(test_text1)
        actual_test_result1 = self.icd10TextTokenGenerator.process_each_token(test_result1)
        graph_nodes = self.icd10TextGraphGenerator.process_token_to_create_graph(actual_test_result1)
        assert graph_nodes['he'][22].pos_tracking[22] == 22
        assert graph_nodes['he'][57].pos_tracking[57] == 57
        assert  graph_nodes['he'][22].length == 2
        assert graph_nodes['he'][22].is_root == True
        assert  graph_nodes['he'][22].parent_token == ""
        assert graph_nodes.get(",", None) == None

    def test_graph_dict_from_token_should_return_proper_datastructure_third_set(self) -> None:
        self.icd10TextTokenGenerator = ICD10TextAndSpanGenerationServiceImpl()
        self.icd10TextGraphGenerator = ICD10GenerateGraphFromTextImpl()
        test_text1 = "He said his ulcerative colitis flares up and giveshim a hard time doing is school work or job work." \
        " His abdominal pain, N / V comes and goes; sometiomessevere."
        test_result1 = self.icd10TextTokenGenerator.get_token_with_span(test_text1)
        actual_test_result1 = self.icd10TextTokenGenerator.process_each_token(test_result1)
        graph_nodes = self.icd10TextGraphGenerator.process_token_to_create_graph(actual_test_result1)
        assert graph_nodes['work'][82].pos_tracking[82] == 82
        assert graph_nodes['work'][94].pos_tracking[94] == 94
        assert graph_nodes['work'][94].parent_token == ""
        assert graph_nodes['work'][94].is_root == True
        assert  graph_nodes['work'][82].length == 4
        assert graph_nodes['work'][82].is_root == True
        assert  graph_nodes['work'][82].parent_token == ""
        assert graph_nodes.get(",", None) == None