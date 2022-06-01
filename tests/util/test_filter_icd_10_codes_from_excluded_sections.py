from unittest import TestCase

from app.dto.pipeline.excluded_sections.family_history_excluded_section import FamilyHistorySection
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.util.icd_10_filter_util import ICD10FilterUtil


class TestFilterICD10CodesServiceFromExcludedSections(TestCase):
    def test__get_filtered_annotations_based_on_excluded_sections__given_correct_family_history_section__excludes_icd_10_codes(
            self):
        dummy_icd10_annotation = self.__get_dummy_icd10_data()

        filtered_icd10_annotations_from_excluded_sections = ICD10FilterUtil.get_filtered_annotations_based_on_excluded_sections(
            dummy_icd10_annotation, self.__get_family_history_section()
        )

        assert filtered_icd10_annotations_from_excluded_sections[0] == dummy_icd10_annotation[1]

    def __get_family_history_section(self):
        section1 = FamilyHistorySection(start=10, end=25)
        section2 = FamilyHistorySection(start=38, end=53)

        return [section1, section2]

    def test_is_icd10_term_valid__given_correct_input__should_return_correct_response(self):
        mock_icd10_annotation_result = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=11,
                                                             end_offset=15, is_negated=False, score=0.7,
                                                             suggested_codes=[],
                                                             raw_acm_response={"data": "data"})

        assert ICD10FilterUtil.is_icd10_term_valid(mock_icd10_annotation_result, 0.85) is False

        mock_icd10_annotation_result.medical_condition = "sick"
        mock_icd10_annotation_result.score = 1.0

        assert ICD10FilterUtil.is_icd10_term_valid(mock_icd10_annotation_result, 0.85) is False

        mock_icd10_annotation_result.medical_condition = "SICK"
        mock_icd10_annotation_result.score = 0.7

        assert ICD10FilterUtil.is_icd10_term_valid(mock_icd10_annotation_result, 0.85) is False

        mock_icd10_annotation_result.medical_condition = "Tuberculosis"
        mock_icd10_annotation_result.score = 0.7
        mock_icd10_annotation_result.is_negated = True

        assert ICD10FilterUtil.is_icd10_term_valid(mock_icd10_annotation_result, 0.85) is False

        mock_icd10_annotation_result.medical_condition = "Tuberculosis"
        mock_icd10_annotation_result.score = 0.9
        mock_icd10_annotation_result.is_negated = False

        assert ICD10FilterUtil.is_icd10_term_valid(mock_icd10_annotation_result, 0.85) is True

    def __get_dummy_icd10_data(self):
        icd10_annotation_1 = ICD10Annotation(code="A15.0", description="Tuberculosis of lung", score=0.7)
        icd10_annotation_2 = ICD10Annotation(code="A15.9", description="Respiratory tuberculosis unspecified",
                                             score=0.54)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="Affect is normal", begin_offset=12,
                                                          end_offset=24, is_negated=False,
                                                          suggested_codes=[icd10_annotation_1, icd10_annotation_2],
                                                          raw_acm_response={"data": "data"})

        icd10_annotation_3 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_4 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)

        icd10_annotation_result_2 = ICD10AnnotationResult(medical_condition="sleeping well", begin_offset=54,
                                                          end_offset=64, is_negated=True,
                                                          suggested_codes=[icd10_annotation_3, icd10_annotation_4],
                                                          raw_acm_response={"data": "data"})

        icd10_annotation_5 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_6 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)

        icd10_annotation_result_3 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=40,
                                                          end_offset=50, is_negated=False,
                                                          suggested_codes=[icd10_annotation_5, icd10_annotation_6],
                                                          raw_acm_response={"data": "data"})

        return [icd10_annotation_result_1, icd10_annotation_result_2, icd10_annotation_result_3]
