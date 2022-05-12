from unittest import TestCase

from app.util.text_postprocessor_util import TextPostProcessorUtil
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult


class TestTextPostprocessorUtil(TestCase):
    def test__get_postprocessed_text__should_return_postprocessed_text__given_correct_input(self):
        mock_icd10_annotations = self.__get_dummy_icd10_data()
        mock_text_length = 68

        post_processed_icd10_annotations = TextPostProcessorUtil.get_icd10_annotations_with_post_processed_text(mock_icd10_annotations, mock_text_length)

        assert post_processed_icd10_annotations[2].medical_condition[-1] == 's'
        assert post_processed_icd10_annotations[2].end_offset == 68

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

        icd10_annotation_result_3 = ICD10AnnotationResult(medical_condition="Tuberculosis,", begin_offset=65,
                                                              end_offset=69, is_negated=False,
                                                              suggested_codes=[icd10_annotation_5, icd10_annotation_6],
                                                              raw_acm_response={"data": "data"})

        return [icd10_annotation_result_1, icd10_annotation_result_2, icd10_annotation_result_3]
