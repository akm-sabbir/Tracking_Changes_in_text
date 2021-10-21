from unittest import TestCase
from unittest.mock import Mock, call, patch

from app.dto.core.pipeline.acm_icd10_response import ACMICD10Result
from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.impl.amazon_icd10_annotator_service import AmazonICD10AnnotatorServiceImpl
from app.service.pipeline.components.acm_icd10_annotation_component import ACMICD10AnnotationComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent


class TestICD10AnnotationComponent(TestCase):
    @patch("app.service.impl.amazon_icd10_annotator_service.boto3", Mock())
    @patch("app.service.impl.dynamo_db_service.boto3", Mock())
    @patch("app.util.config_manager.ConfigManager.get_specific_config", Mock())
    def test__run__should_return_correct_response__given_correct_input(self):
        paragraph1 = Paragraph("some text", 0, 10)
        paragraph2 = Paragraph("some other text", 11, 20)
        mock_icd10_service = Mock(AmazonICD10AnnotatorServiceImpl)
        icd10_annotation_component = ACMICD10AnnotationComponent()

        mock_save_item = Mock()
        mock_save_item.return_value = True
        mock_db_service = Mock()
        mock_db_service.save_item = mock_save_item

        icd10_annotation_component._ACMICD10AnnotationComponent__icd10_annotation_service = mock_icd10_service
        icd10_annotation_component._ACMICD10AnnotationComponent__db_service = mock_db_service

        mock_icd10_service.get_icd_10_codes = Mock()
        mock_icd10_service.get_icd_10_codes.side_effect = self.__get_dummy_icd10_data()

        acm_result: ACMICD10Result = icd10_annotation_component.run(
            {NotePreprocessingComponent: [paragraph1, paragraph2], "acm_cached_result": None, "id": "123"})[0]
        calls = [call("some text"), call("some other text")]
        mock_icd10_service.get_icd_10_codes.assert_has_calls(calls)
        assert mock_icd10_service.get_icd_10_codes.call_count == 2

        icd10_result = acm_result.icd10_annotations
        assert acm_result.id == "123"

        assert icd10_result[0].begin_offset == 12
        assert icd10_result[0].end_offset == 24
        assert icd10_result[0].medical_condition == "Tuberculosis"

        assert icd10_result[0].suggested_codes[0].code == "A15.0"
        assert icd10_result[0].suggested_codes[0].description == "Tuberculosis of lung"
        assert icd10_result[0].suggested_codes[0].score == 0.7

        assert icd10_result[0].suggested_codes[1].code == "A15.9"
        assert icd10_result[0].suggested_codes[1].description == "Respiratory tuberculosis unspecified"
        assert icd10_result[0].suggested_codes[1].score == 0.54

        assert icd10_result[1].begin_offset == 56
        assert icd10_result[1].end_offset == 65
        assert icd10_result[1].medical_condition == "pneumonia"

        assert icd10_result[1].suggested_codes[0].code == "J12.0"
        assert icd10_result[1].suggested_codes[0].description == "Adenoviral pneumonia"
        assert icd10_result[1].suggested_codes[0].score == 0.89

        assert icd10_result[1].suggested_codes[1].code == "J12.89"
        assert icd10_result[1].suggested_codes[1].description == "Other viral pneumonia"
        assert icd10_result[1].suggested_codes[1].score == 0.45

    @patch("app.service.impl.amazon_icd10_annotator_service.boto3", Mock())
    @patch("app.service.impl.dynamo_db_service.boto3", Mock())
    @patch("app.util.config_manager.ConfigManager.get_specific_config", Mock())
    def test__run__should_return_correct_response__given_correct_input_and_cached_data(self):
        paragraph1 = Paragraph("some text", 0, 10)
        paragraph2 = Paragraph("some other text", 11, 20)
        mock_icd10_service = Mock(AmazonICD10AnnotatorServiceImpl)
        icd10_annotation_component = ACMICD10AnnotationComponent()

        mock_save_item = Mock()
        mock_save_item.return_value = True
        mock_db_service = Mock()
        mock_db_service.save_item = mock_save_item

        icd10_annotation_component._ACMICD10AnnotationComponent__icd10_annotation_service = mock_icd10_service
        icd10_annotation_component._ACMICD10AnnotationComponent__db_service = mock_db_service

        mock_icd10_service.get_icd_10_codes = Mock()
        mock_icd10_service.get_icd_10_codes.side_effect = self.__get_dummy_icd10_data()
        dummy_result = ACMICD10Result("123", [item for sublist in self.__get_dummy_icd10_data() for item in sublist])
        acm_result: ACMICD10Result = icd10_annotation_component.run(
            {NotePreprocessingComponent: [paragraph1, paragraph2], "acm_cached_result": [dummy_result], "id": "123"})[0]

        mock_icd10_service.get_icd_10_codes.assert_not_called()

        icd10_result = acm_result.icd10_annotations
        assert acm_result.id == "123"

        assert icd10_result[0].begin_offset == 12
        assert icd10_result[0].end_offset == 24
        assert icd10_result[0].medical_condition == "Tuberculosis"

        assert icd10_result[0].suggested_codes[0].code == "A15.0"
        assert icd10_result[0].suggested_codes[0].description == "Tuberculosis of lung"
        assert icd10_result[0].suggested_codes[0].score == 0.7

        assert icd10_result[0].suggested_codes[1].code == "A15.9"
        assert icd10_result[0].suggested_codes[1].description == "Respiratory tuberculosis unspecified"
        assert icd10_result[0].suggested_codes[1].score == 0.54

        assert icd10_result[1].begin_offset == 45
        assert icd10_result[1].end_offset == 54
        assert icd10_result[1].medical_condition == "pneumonia"

        assert icd10_result[1].suggested_codes[0].code == "J12.0"
        assert icd10_result[1].suggested_codes[0].description == "Adenoviral pneumonia"
        assert icd10_result[1].suggested_codes[0].score == 0.89

        assert icd10_result[1].suggested_codes[1].code == "J12.89"
        assert icd10_result[1].suggested_codes[1].description == "Other viral pneumonia"
        assert icd10_result[1].suggested_codes[1].score == 0.45

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

        icd10_annotation_result_2 = ICD10AnnotationResult(medical_condition="pneumonia", begin_offset=45, end_offset=54,
                                                          is_negated=True,
                                                          suggested_codes=[icd10_annotation_3, icd10_annotation_4])

        return [[icd10_annotation_result_1], [icd10_annotation_result_2]]
