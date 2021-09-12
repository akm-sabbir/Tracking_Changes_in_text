from unittest import TestCase

from app.service.pipeline.components.icd10_annotation_dummy_component import ICD10AnnotationDummyComponent


class TestICD10AnnotationDummyComponent(TestCase):
    def test__run__should_return_correct_response__given_correct_input(self):
        result = ICD10AnnotationDummyComponent().run({})
        assert result[0].begin_offset == 12
        assert result[0].end_offset == 24
        assert result[0].medical_condition == "Tuberculosis"

        assert result[0].suggested_codes[0].code == "A15.0"
        assert result[0].suggested_codes[0].description == "Tuberculosis of lung"
        assert result[0].suggested_codes[0].score == 0.7

        assert result[0].suggested_codes[1].code == "A15.9"
        assert result[0].suggested_codes[1].description == "Respiratory tuberculosis unspecified"
        assert result[0].suggested_codes[1].score == 0.54

        assert result[1].begin_offset == 45
        assert result[1].end_offset == 54
        assert result[1].medical_condition == "pneumonia"

        assert result[1].suggested_codes[0].code == "J12.0"
        assert result[1].suggested_codes[0].description == "Adenoviral pneumonia"
        assert result[1].suggested_codes[0].score == 0.89

        assert result[1].suggested_codes[1].code == "J12.89"
        assert result[1].suggested_codes[1].description == "Other viral pneumonia"
        assert result[1].suggested_codes[1].score == 0.45
