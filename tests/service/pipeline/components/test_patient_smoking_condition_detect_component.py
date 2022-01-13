from unittest import TestCase
from app.service.pipeline.components.icd10_smoking_pattern_detection import PatientSmokingConditionDetectionComponent
from app.dto.pipeline.smoker_condition import PatientSmokingCondition


class Icd10SmokingPatternDetectionTest(TestCase):

    smoking_pattern_detect_comp: PatientSmokingConditionDetectionComponent

    def test_run_should_return_bool(self):
        self.smoking_pattern_detect_comp = PatientSmokingConditionDetectionComponent()
        text = "as the patient queried about smoking behavior? Yes No\n"
        "Does the patient currently smoke? Smoking: Patient has never smoked - (1/21/2020).\n"
        not_smoker: PatientSmokingCondition = self.smoking_pattern_detect_comp.run({"text": text})
        assert not_smoker.notSmoker is True