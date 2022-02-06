from unittest import TestCase
from app.service.pipeline.components.icd10_smoking_pattern_detection import PatientSmokingConditionDetectionComponent
from app.dto.pipeline.smoker_condition import PatientSmokingCondition
from tests.service.impl.dummy_smoking_pattern_decision_model import Negation, DummySciSpacyModel, Doc
from app.dto.pipeline.Smoker import Smoker


class Icd10SmokingPatternDetectionTest(TestCase):

    def test_1_run_should_return_bool(self):

        dummy_model_1 = DummySciSpacyModel()
        smoking_pattern_detect_comp = PatientSmokingConditionDetectionComponent(dummy_model_1.nlp_process)
        dummy_model_1.set_doc_entity_polarity(polarity=True)
        text = "as the patient queried about smoking behavior? Yes No\n" \
               "Does the patient currently smoke? Smoking: Patient has never smoked - (1/21/2020).\n"
        _smoker: [PatientSmokingCondition] = smoking_pattern_detect_comp.run({"text": text})
        assert _smoker[0].isSmoker == Smoker.NOT_SMOKER

    def test_2_run_should_return_bool(self):
        dummy_model_2 = DummySciSpacyModel()
        dummy_model_2.set_doc_entity_polarity(polarity=False)
        smoking_pattern_detect_comp = PatientSmokingConditionDetectionComponent(dummy_model_2.nlp_process)
        text1 = "Was the patient queried about smoking behavior? Yes No\n" \
               "Does the patient currently smoke? Smoking: Light tobacco smoker (10 or fewer cigarettes/day) -"
        dic_ = {"text" : text1}
        _smoker: [PatientSmokingCondition] = smoking_pattern_detect_comp.run(dic_)
        assert _smoker[0].isSmoker == Smoker.SMOKER

    def test_3_run_should_return_bool(self):
        dummy_model_3 = DummySciSpacyModel()
        smoking_pattern_detect_comp = PatientSmokingConditionDetectionComponent(dummy_model_3.nlp_process)
        text3 = "Current Meds Prior to Visit: Amitriptyline HCL 10 mg 1 by mouth every night at bedtime, " \
                "Amoxicillin 500 mg 1 cap by\n mouth three times a day, Folic Acid 1 mg 1 by mouth every day, " \
                "Metoprolol \n Succinate ER 25 mg 1 by mouth every day, Thiamine HCL 100 mg 1 by mouth every day"
        _smoker: [PatientSmokingCondition] = smoking_pattern_detect_comp.run({"text": text3})
        assert _smoker[0].isSmoker == Smoker.DONT_KNOW

    def test_4_run_should_return_bool(self):
        dummy_model_4 = DummySciSpacyModel()
        smoking_pattern_detect_comp = PatientSmokingConditionDetectionComponent(dummy_model_4.nlp_process)
        dummy_model_4.set_doc_entity_polarity(polarity=False)

        text4 = "Was the patient queried about smoking behavior? Yes No\n"\
                "Does the patient currently smoke? . (Smoking Hx)"
        _smoker: [PatientSmokingCondition] = smoking_pattern_detect_comp.run({"text": text4})
        assert _smoker[0].isSmoker == Smoker.SMOKER

    def test_5_run_should_return_bool(self):
        dummy_model_5 = DummySciSpacyModel()
        smoking_pattern_detect_comp = PatientSmokingConditionDetectionComponent(dummy_model_5.nlp_process)
        text4 = "Was the patient queried about smoking behavior? Yes No\n" \
                "Does the patient currently smoke? . (Hx)"
        _smoker: [PatientSmokingCondition] = smoking_pattern_detect_comp.run({"text": text4})
        print(_smoker[0].isSmoker)
        assert _smoker[0].isSmoker == Smoker.DONT_KNOW