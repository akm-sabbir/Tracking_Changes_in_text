from unittest import TestCase
from unittest.mock import patch, Mock
from app.service.impl.icd10_smoking_pattern_decision_impl import ICD10SmokingPatternDecisionImpl
from app.settings import Settings
from tests.service.impl.dummy_smoking_pattern_decision_model import DummySciSpacyModel


class TestICD10SmokingPatternDecisionImpl(TestCase):
    icd10SmokingPatternDetect: ICD10SmokingPatternDecisionImpl

    def test_get_smoking_pattern_decision_should_return_true_if_no_smoker(self) -> None:
        dummy_model = DummySciSpacyModel()
        self.icd10SmokingPatternDetect = ICD10SmokingPatternDecisionImpl(dummy_model.nlp_process)
        text = "as the patient queried about smoking behavior? Yes No\n" \
               "Does the patient currently smoke? Smoking: Patient has never smoked - (1/21/2020).\n"
        results = self.icd10SmokingPatternDetect.get_smoking_pattern_decision(text)
        assert results == -1