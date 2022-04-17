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
        assert len(graph_nodes['patient'].pos_list) == 2
        assert graph_nodes['patient'].pos_tracking[7] == 7
        assert graph_nodes['patient'].pos_tracking[63] == 63
        assert  graph_nodes['patient'].length == 7
        assert graph_nodes['patient'].pos_list[0].start == 7
        assert graph_nodes['patient'].pos_list[0].end == 14
        assert  graph_nodes['patient'].parent_token == ""
        assert graph_nodes.get("?", None) == None
        assert graph_nodes['patient'].is_root == True
        assert graph_nodes['1/21/2020'].length == 9

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
        assert len(graph_nodes['he'].pos_list) == 12
        assert graph_nodes['he'].pos_tracking[22] == 22
        assert graph_nodes['he'].pos_tracking[57] == 57
        assert graph_nodes['he'].pos_list[0].start == 22
        assert graph_nodes['he'].pos_list[0].end == 24
        assert graph_nodes['he'].pos_list[1].start == 57
        assert graph_nodes['he'].pos_list[1].end == 59
        assert  graph_nodes['he'].length == 2
        assert graph_nodes['he'].is_root == True
        assert  graph_nodes['he'].parent_token == ""
        assert graph_nodes.get(",", None) == None
        assert graph_nodes['he'].track_pos == 0

    def test_graph_dict_from_token_should_return_proper_datastructure_third_set(self) -> None:
        self.icd10TextTokenGenerator = ICD10TextAndSpanGenerationServiceImpl()
        self.icd10TextGraphGenerator = ICD10GenerateGraphFromTextImpl()
        test_text1 = "He said his ulcerative colitis flares up and giveshim a hard time doing is school work or job work." \
        " His abdominal pain, N / V comes and goes; sometiomessevere."
        test_result1 = self.icd10TextTokenGenerator.get_token_with_span(test_text1)
        actual_test_result1 = self.icd10TextTokenGenerator.process_each_token(test_result1)
        graph_nodes = self.icd10TextGraphGenerator.process_token_to_create_graph(actual_test_result1)
        assert len(graph_nodes['work'].pos_list) == 2
        assert graph_nodes['work'].pos_tracking[82] == 82
        assert graph_nodes['work'].pos_tracking[94] == 94
        assert graph_nodes['work'].pos_list[0].start == 82
        assert graph_nodes['work'].pos_list[0].end == 86
        assert  graph_nodes['work'].length == 4
        assert graph_nodes['work'].is_root == True
        assert  graph_nodes['work'].parent_token == ""
        assert graph_nodes.get(",", None) == None
        assert graph_nodes['work'].track_pos == 0