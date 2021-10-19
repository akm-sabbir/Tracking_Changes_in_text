from unittest import TestCase
from unittest.mock import Mock, call, patch

from app.dto.core.paragraph import Paragraph
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.impl.amazon_icd10_annotator_service import AmazonICD10AnnotatorServiceImpl
from app.service.pipeline.components.icd10_annotation_component import ICD10AnnotationComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.service.pipeline.components.icd10_annotation_filter_component import  ICD10AnnotationAlgoComponent
from app.service.impl.icd10_annotation_service_with_filters_impl import ICD10AnnotatorServiceWithFilterImpl
from app.service.pipeline.components.icd10_to_hcc_annotation import ICD10ToHccAnnotationComponent


class TestICD10AnnotationAlgoComponent(TestCase):
    @patch("app.service.impl.amazon_icd10_annotator_service.boto3")
    def test__run__should_return_correct_response__given_correct_input(self, mock_boto3):
        paragraph1 = Paragraph("some text", 0, 10)
        paragraph2 = Paragraph("some other text", 11, 20)
        mock_icd10_service = Mock(AmazonICD10AnnotatorServiceImpl)
        icd10_annotation_component = ICD10AnnotationComponent()
        icd10_annotation_filter_component = ICD10AnnotationAlgoComponent()
        icd10_annotation_component._ICD10AnnotationComponent__icd10_annotation_service = mock_icd10_service
        icd10_annotation_filter_component._ICD10AnnotationAlgoComponent____icd10_annotation_service_with_filters = \
            Mock(ICD10AnnotatorServiceWithFilterImpl)
        mock_icd10_service.get_icd_10_codes = Mock()
        mock_icd10_service.get_icd_10_codes.side_effect = self.__get_dummy_icd10_data()

        params = {"dx_threshold": 0.9, "icd10_threshold": 0.67, "parent_threshold":0.80,
                  ICD10AnnotationComponent:self.__get_dummy_icd10_data(),
                  ICD10ToHccAnnotationComponent:{}}
        results = icd10_annotation_filter_component.run(params)

        assert results[0].suggested_codes[0].code == "A15.0"
        assert results[0].suggested_codes[0].description == "Tuberculosis of lung"
        assert results[0].suggested_codes[0].score == 0.7

        assert results[1].medical_condition == "pneumonia"

        assert results[1].suggested_codes[0].code == "J12.0"
        assert results[1].suggested_codes[0].description == "Adenoviral pneumonia"
        assert results[1].suggested_codes[0].score == 0.89

    def __get_dummy_icd10_data(self):
        icd10_annotation_1 = ICD10Annotation(code="A15.0", description="Tuberculosis of lung", score=0.7)
        icd10_annotation_2 = ICD10Annotation(code="A15.9", description="Respiratory tuberculosis unspecified",
                                             score=0.54)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=12,
                                                          end_offset=24, is_negated=False,
                                                          suggested_codes=[icd10_annotation_1, icd10_annotation_2])

        icd10_annotation_3 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_4 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)
        icd10_annotation_5 = ICD10Annotation(code="J12", description="Other viral pneumonia",
                                             score=0.72)

        icd10_annotation_result_2 = ICD10AnnotationResult(medical_condition="pneumonia", begin_offset=45, end_offset=54,
                                                          is_negated=True,
                                                          suggested_codes=[icd10_annotation_3, icd10_annotation_4,
                                                                           icd10_annotation_5])

        return [icd10_annotation_result_1, icd10_annotation_result_2]
