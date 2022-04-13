from unittest import TestCase
from unittest.mock import patch, Mock
from app.service.impl.icd10_text_token_span_gen_service_impl import ICD10TextAndSpanGenerationServiceImpl


class TestICD10TextAndSpanGenerationServiceImplTest(TestCase):
    icd10TextTokenGenerator: ICD10TextAndSpanGenerationServiceImpl

    def test__get_text_tokenized_and_span_should_return_proper_data(self) -> None:
        self.icd10TextTokenGenerator = ICD10TextAndSpanGenerationServiceImpl()
        test_text1 = "as the patient queried about smoking behavior? Yes No\n" \
               "Does the patient currently smoke? Smoking: Patient has never smoked - (1/21/2020).\n"
        test_result1 = self.icd10TextTokenGenerator.get_token_with_span(test_text1)
        actual_test_result1 = self.icd10TextTokenGenerator.process_each_token(test_result1)
        print(actual_test_result1)
        count = sum([1 if actual_test_result1[i][0] == '?' else 0 for i in range(len(actual_test_result1))])
        count_paren = sum([1 if actual_test_result1[i][0] == '(' else 0 for i in range(len(actual_test_result1))])
        count_colon = sum([1 if actual_test_result1[i][0] == '(' else 0 for i in range(len(actual_test_result1))])
        assert count == 2
        assert count_paren == 1
        assert count_colon == 1
        assert actual_test_result1[2][1] == 7
        assert actual_test_result1[2][2] == 14
        assert actual_test_result1[6][0] == "behavior"

    def test__get_text_tokenized_and_span_should_return_proper_data_second_set(self) -> None:
        self.icd10TextTokenGenerator = ICD10TextAndSpanGenerationServiceImpl()
        test_text1 = "He has alot going on, he continues to drinks, daily, " \
           "and he has been feeling dizzy with some fall,he was in the er recently " \
           "and he had a head CT, he still smokes, coughing wheezying breathless, withsputum, " \
           "he stil has urinary incontinent, he has been confirmed to have colon cancer, " \
           "he am not sure he has hallucinations, he not sleeping well, he has chronic urinary and bowel incontinent, " \
           "he also chronic diarrheafrom time to time,  the absence of recurrent leg cramps is obvious"
        test_result1 = self.icd10TextTokenGenerator.get_token_with_span(test_text1)
        actual_test_result1 = self.icd10TextTokenGenerator.process_each_token(test_result1)
        count = sum([1 if actual_test_result1[i][0] == ',' else 0 for i in range(len(actual_test_result1))])
        assert actual_test_result1[2][1] == 7
        assert actual_test_result1[2][2] == 11
        assert actual_test_result1[7][0] == "continues"
        assert  actual_test_result1[11][0] == "daily"
        assert actual_test_result1[21][0] == 'fall'
        assert actual_test_result1[50][0] == 'incontinent'
        assert count == 14

    def test__get_text_tokenized_and_span_should_return_proper_data_second_set(self):
        self.icd10TextTokenGenerator = ICD10TextAndSpanGenerationServiceImpl()
        test_text2= "He said his ulcerative colitis flares up and giveshim a hard time doing is school work or job work." \
        " His abdominal pain, N / V comes and goes; sometiomessevere."
        test_result2 = self.icd10TextTokenGenerator.get_token_with_span(test_text2)
        actual_test_result2 = self.icd10TextTokenGenerator.process_each_token(test_result2)
        count = sum([1 if actual_test_result2[i][0] == '/' else 0 for i in range(len(actual_test_result2))])
        assert actual_test_result2[2][1] == 8
        assert actual_test_result2[2][2] == 11
        assert actual_test_result2[30][0] == ";"
        assert count == 1