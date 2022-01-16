from unittest import TestCase
from app.service.pipeline.components.icd10_smoking_pattern_detection import PatientSmokingConditionDetectionComponent
from app.dto.pipeline.smoker_condition import PatientSmokingCondition
from tests.service.impl.dummy_smoking_pattern_decision_model import Negation,DummySciSpacyModel,Doc


class Icd10SmokingPatternDetectionTest(TestCase):

    smoking_pattern_detect_comp: PatientSmokingConditionDetectionComponent

    def test_run_should_return_bool(self):
        dummy_model = DummySciSpacyModel()
        self.smoking_pattern_detect_comp = PatientSmokingConditionDetectionComponent(dummy_model.nlp_process)
        text = "as the patient queried about smoking behavior? Yes No\n" \
               "Does the patient currently smoke? Smoking: Patient has never smoked - (1/21/2020).\n"
        not_smoker: [PatientSmokingCondition] = self.smoking_pattern_detect_comp.run({"text": text})
        print(not_smoker[0].notSmoker)
        assert not_smoker[0].notSmoker is True