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
        print(test_result1)
        actual_test_result1 = self.icd10TextTokenGenerator.process_each_token(test_result1)
        assert actual_test_result1[2][1] == 7
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
        assert actual_test_result1[2][1] == 7
        assert actual_test_result1[6][0] == "continues"
        assert  actual_test_result1[18][0] == 'fall'