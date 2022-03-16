from typing import List
from unittest import TestCase

from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.util.span_merger_util import SpanMergerUtil


class TestSpanMergerUtil(TestCase):
    def test__get_icd_10_codes_with_relevant_spans__should_return_correct_response__given_correct_input(self):
        mock_icd10_annotations = self.__get_dummy_icd10_annotation_result()
        no_of_components_in_algorithm = 3

        icd10_filtered_annotations = SpanMergerUtil.get_icd_10_codes_with_relevant_spans(mock_icd10_annotations,
                                                                                         no_of_components_in_algorithm)


        assert icd10_filtered_annotations[0].begin_offset == 0
        assert icd10_filtered_annotations[0].end_offset == 7

        assert icd10_filtered_annotations[1].begin_offset == 8
        assert icd10_filtered_annotations[1].end_offset == 10

        assert icd10_filtered_annotations[2].begin_offset == 50
        assert icd10_filtered_annotations[2].end_offset == 130

        assert icd10_filtered_annotations[3].begin_offset == 300
        assert icd10_filtered_annotations[3].end_offset == 900

        assert icd10_filtered_annotations[3].suggested_codes[0].code == 'A15.0'
        assert icd10_filtered_annotations[3].suggested_codes[1].code == 'J12.89'
        assert icd10_filtered_annotations[3].suggested_codes[2].code == 'A15.9'


    def __get_dummy_icd10_annotation_result(self) -> List[ICD10AnnotationResult]:
        icd10_annotation_1 = ICD10Annotation(code="A15.0", description="Tuberculosis of lung", score=0.7)
        icd10_annotation_2 = ICD10Annotation(code="A15.9", description="Respiratory tuberculosis unspecified",
                                             score=0.54)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=600,
                                                          end_offset=900, is_negated=False,
                                                          suggested_codes=[icd10_annotation_1, icd10_annotation_2],
                                                          raw_acm_response={"data": "data"})

        icd10_annotation_3 = ICD10Annotation(code="A15.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_4 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)

        icd10_annotation_result_2 = ICD10AnnotationResult(medical_condition="pneumonia", begin_offset=460,
                                                          end_offset=700,
                                                          is_negated=False,
                                                          suggested_codes=[icd10_annotation_3, icd10_annotation_4],
                                                          raw_acm_response={"data": "data"})

        icd10_annotation_5 = ICD10Annotation(code="A15.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_6 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)

        icd10_annotation_result_3 = ICD10AnnotationResult(medical_condition="pneumonia", begin_offset=300,
                                                          end_offset=500,
                                                          is_negated=False,
                                                          suggested_codes=[icd10_annotation_5, icd10_annotation_6],
                                                          raw_acm_response={"data": "data"})

        icd10_annotation_7 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_8 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)

        icd10_annotation_result_4 = ICD10AnnotationResult(medical_condition="pneumonia", begin_offset=70,
                                                          end_offset=130,
                                                          is_negated=False,
                                                          suggested_codes=[icd10_annotation_7, icd10_annotation_8],
                                                          raw_acm_response={"data": "data"})

        icd10_annotation_9 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_10 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                              score=0.45)

        icd10_annotation_result_5 = ICD10AnnotationResult(medical_condition="pneumonia", begin_offset=60,
                                                          end_offset=120,
                                                          is_negated=False,
                                                          suggested_codes=[icd10_annotation_9, icd10_annotation_10],
                                                          raw_acm_response={"data": "data"})

        icd10_annotation_11 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_12 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                              score=0.45)

        icd10_annotation_result_6 = ICD10AnnotationResult(medical_condition="pneumonia", begin_offset=50,
                                                          end_offset=100,
                                                          is_negated=False,
                                                          suggested_codes=[icd10_annotation_11, icd10_annotation_12],
                                                          raw_acm_response={"data": "data"})

        icd10_annotation_13 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_14 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                              score=0.45)

        icd10_annotation_result_7 = ICD10AnnotationResult(medical_condition="pneumonia", begin_offset=0, end_offset=7,
                                                          is_negated=False,
                                                          suggested_codes=[icd10_annotation_13, icd10_annotation_14],
                                                          raw_acm_response={"data": "data"})

        icd10_annotation_15 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_16 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                              score=0.45)

        icd10_annotation_result_8 = ICD10AnnotationResult(medical_condition="pneumonia", begin_offset=8, end_offset=10,
                                                          is_negated=False,
                                                          suggested_codes=[icd10_annotation_15, icd10_annotation_16],
                                                          raw_acm_response={"data": "data"})

        return [icd10_annotation_result_1, icd10_annotation_result_2, icd10_annotation_result_3,
                icd10_annotation_result_4, icd10_annotation_result_5, icd10_annotation_result_6,
                icd10_annotation_result_7, icd10_annotation_result_8]
