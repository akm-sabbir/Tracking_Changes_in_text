from unittest import TestCase
from unittest.mock import patch, Mock

from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.icd10_positive_sentiment_exclusion_service import ICD10SentimentExclusionService
from app.service.impl.icd10_positive_sentiment_exclusion_service_impl import ICD10SentimentExclusionServiceImpl


class TestICD10SentimentExclusionServiceImpl(TestCase):
    @patch('app.settings.Settings.get_sentiments_set')
    def test_get_filtered_annotations_based_on_positive_sentiment__should_return_correct_response__given_correct_input(
            self, get_sentiments_set: Mock):

        get_sentiments_set.return_value = self.__get_positive_sentiment_exclusion()

        icd10_positive_sentiment_exclusion: ICD10SentimentExclusionService = ICD10SentimentExclusionServiceImpl()

        mock_filtered_icd10_list = icd10_positive_sentiment_exclusion.get_filtered_annotations_based_on_positive_sentiment(
            self.__get_dummy_icd10_data())

        get_sentiments_set.assert_called_once()

        assert mock_filtered_icd10_list[0].medical_condition == "sleeping well"
        assert mock_filtered_icd10_list[1].medical_condition == "Tuberculosis"

    def __get_positive_sentiment_exclusion(self):
        return {"good", "well", "better", "fine", "pleasant", "comfortable", "healthy", "normal", "comfort", "fair",
                "clear"}

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

        icd10_annotation_result_2 = ICD10AnnotationResult(medical_condition="sleeping well", begin_offset=45, end_offset=54,
                                                          is_negated=True,
                                                          suggested_codes=[icd10_annotation_3, icd10_annotation_4],
                                                          raw_acm_response={"data": "data"})

        icd10_annotation_5 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_6 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)

        icd10_annotation_result_3 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=40, end_offset=50,
                                                          is_negated=False,
                                                          suggested_codes=[icd10_annotation_5, icd10_annotation_6],
                                                          raw_acm_response={"data": "data"})

        return [icd10_annotation_result_1, icd10_annotation_result_2, icd10_annotation_result_3]
