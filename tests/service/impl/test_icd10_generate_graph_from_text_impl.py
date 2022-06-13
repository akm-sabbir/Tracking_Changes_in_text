from unittest import TestCase
from unittest.mock import patch, Mock

from app.dto.pipeline.tokenization_component_result import TokenizationResult
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
        graph_nodes = self.icd10TextGraphGenerator.process_token_to_create_graph(TokenizationResult(actual_test_result1))
        assert graph_nodes['patient'][7].pos_tracking == 7
        assert graph_nodes['patient'][63].pos_tracking == 63
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
        graph_nodes = self.icd10TextGraphGenerator.process_token_to_create_graph(TokenizationResult(actual_test_result1))
        assert graph_nodes['he'][22].pos_tracking == 22
        assert graph_nodes['he'][57].pos_tracking == 57
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
        graph_nodes = self.icd10TextGraphGenerator.process_token_to_create_graph(TokenizationResult(actual_test_result1))
        assert graph_nodes['work'][82].pos_tracking == 82
        assert graph_nodes['work'][94].pos_tracking == 94
        assert graph_nodes['work'][94].parent_token == ""
        assert graph_nodes['work'][94].is_root == True
        assert  graph_nodes['work'][82].length == 4
        assert graph_nodes['work'][82].is_root == True
        assert  graph_nodes['work'][82].parent_token == ""
        assert graph_nodes.get(",", None) == None

    def test_graph_dict_from_token_should_return_proper_datastructure_fourth_set(self) -> None:
        self.icd10TextTokenGenerator = ICD10TextAndSpanGenerationServiceImpl()
        self.icd10TextGraphGenerator = ICD10GenerateGraphFromTextImpl()
        test_text1 = "CC: Patient presents for a Transitional Care Management exam." \
                     "Date Admitted: **********\n" \
                     "Date Discharged: **********\n" \
                     "Living Environment: Patient lives with relatives her mum is currently home here with ***\n"
        "Limitations: Patient has physical de-condition No. Is the patient's hearing okay? Yes. Is the patient's\n"
        "vision okay? Yes. Is the patient's mental status okay? Yes. Does the patient have any dementia? No" \
        "Home Care Services: none\n"
        "Physical/Occupational therapy:\n"
        "Ambulation Status:\n"
        "Continence:\n\n"
        "HPI: s/p elective excisiion og bilateral suppurative hydradenitis, surgery was complicated by sepsis from"
        "c diffle she was admited for 3 days, she now feels much , no more fever, no diarrhea, no\n"
        "breathlessness and the surgial side is healing , but the rt side is leaking some, clear liquid with no smell\n"
        "ROS:\n"
        "Const: Denies chills, fever and sweats.\n"
        "Eyes: Denies a recent change in visual acuity and watery or itching eyes.\n"
        "ENMT: Denies congestion, excessive sneezing and postnasal drip.\n"
        "CV: Denies chest pain, orthopnea, palpitations and swelling of ankles.\n"
        "Resp: Denies cough, PND, SOB, sputum production and wheezing.\n"
        "GI: Denies abdominal pain, constipation, diarrhea, hematemesis, melena, nausea and vomiting.\n"
        "GU: Urinary: denies dysuria, frequency, hematuria and change in urine odor.\n"
        "Skin: Denies rashes.\n"
        "Neuro: Denies headache, loss of consciousness and vertigo.\n\n."
        "Const: Appears moderately overweight. No signs of apparent distress present.\n"
        "Head/Face: Normal on inspection.\n"
        "ENMT: External Ears: Inspection reveals normal ears. Canals WNL. Nasopharynx: Normal to\n"
        "inspection. Dentition is normal. Gums appear healthy. Palate normal in appearance.\n"
        "Neck: Normal to inspection. Normal to palpation. No masses appreciated. No JVD. Carotids: no\n"
        "bruits.\n"
        "Resp: Inspection of chest reveals no chest wall deformity. Percussion is resonant and equal. Lungs\n"
        "are clear bilaterally. Chest is normal to inspection and palpation.\n"
        "CV: No lifts or thrills. PMI is not displaced. S1 is normal. S2 is normal. No extra sounds. No heart\n"
        "murmur appreciated. Extremities: No clubbing, cyanosis or edema.\n"
        "Abdomen: Abdomen is soft, nontender, and nondistended without guarding, rigidity or rebound\n"
        "tenderness. No abdominal masses. No pulsatile masses present. Abdominal wall is soft. No\n"
        "palpable hernias. No palpable hepatosplenomegaly. Kidneys are not palpable.\n"
        "Musculo: Walks with a normal gait. Upper Extremities: Normal to inspection and palpation. Lower\n"
        "Extremities: Normal to inspection and palpation.\n"
        "Skin: Skin is warm and dry. Hair appears normal. healing axilla\n\n."
        test_result1 = self.icd10TextTokenGenerator.get_token_with_span(test_text1)
        actual_test_result1 = self.icd10TextTokenGenerator.process_each_token(test_result1)
        graph_nodes = self.icd10TextGraphGenerator.process_token_to_create_graph(
            TokenizationResult(actual_test_result1))
        assert graph_nodes["Patient"][4].parent_token == ''