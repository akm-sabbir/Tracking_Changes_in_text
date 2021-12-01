import asyncio
from asyncio import AbstractEventLoop
from unittest import TestCase
from unittest.mock import Mock, patch

from pydantic import ValidationError

from app.Settings import Settings
from app.dto.core.icd10_pipeline_params import ICD10PipelineParams
from app.dto.core.service.hcc_code import HCCCode
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.request.icd10_annotation_request import ICD10AnnotationRequest
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.dto.response.icd10_annotation_response import ICD10AnnotationResponse


class Test(TestCase):
    __loop: AbstractEventLoop

    @classmethod
    def setUpClass(cls):
        cls.__loop = asyncio.new_event_loop()

    @classmethod
    def tearDownClass(cls):
        cls.__loop.close()

    @patch("app.util.dependency_injector.DependencyInjector.get_instance")
    def test__annotation_router__given_correct_input__should_return_correct_response(self, mock_get_instance: Mock):
        Settings.dx_threshold = 0.7
        Settings.parent_threshold = 0.7
        Settings.icd10_threshold = 0.7
        Settings.use_cache = True

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

        mock_icd10_results = [icd10_annotation_result_1, icd10_annotation_result_2]

        mock_icd10_service = Mock()
        mock_icd10_service.run_icd10_pipeline = Mock()

        mock_hcc_maps = Mock(HCCResponseDto)
        mock_hcc_maps.hcc_maps = {"A123": HCCCode(code="HCC108", score=0.5)}
        mock_icd10_service.run_icd10_pipeline.return_value = ICD10AnnotationResponse(
            id="123", icd10_annotations=mock_icd10_results, raw_acm_data=[{"acm_data": "data"}], hcc_maps=mock_hcc_maps)
        mock_get_instance.return_value = mock_icd10_service
        from app.router import annotation_router
        response = self.__loop.run_until_complete(
            annotation_router.annotate_icd_10([ICD10AnnotationRequest(id="123", text="text", sex="M", age=70)],
                                              dx_threshold=0.7,
                                              icd10_threshold=0.7, parent_threshold=0.7, use_cache=True))
        assert response[0].icd10_annotations == mock_icd10_results
        call_args: ICD10PipelineParams = mock_icd10_service.run_icd10_pipeline.call_args[0][0]
        assert call_args.note_id == "123"
        assert call_args.text == "text"
        assert call_args.dx_threshold == 0.7
        assert call_args.icd10_threshold == 0.7
        assert call_args.parent_threshold == 0.7

    def test_annotation_router__given_empty_input__should_raise_validation_error(self):
        from app.router import annotation_router
        with self.assertRaises(ValidationError) as error:
            annotation_router.annotate_icd_10([ICD10AnnotationRequest(id="123", text="  ")])
        error_location = error.exception.errors()[0]['loc'][0]
        error_message = error.exception.errors()[0]['msg']
        assert error_location == 'text'
        assert error_message == 'text must be string and cannot be empty'

    @patch("app.util.dependency_injector.DependencyInjector.get_instance")
    def test_annotation_router__given_boolean_text_input__should_raise_validation_error(self, mock_get_instance):
        mock_get_instance.return_value = Mock()
        from app.router import annotation_router
        with self.assertRaises(ValidationError) as error:
            annotation_router.annotate_icd_10([ICD10AnnotationRequest(id="123", text="true")])
        error_location = error.exception.errors()[0]['loc'][0]
        error_message = error.exception.errors()[0]['msg']
        assert error_location == 'text'
        assert error_message == 'text must be string and cannot be empty'

        with self.assertRaises(ValidationError) as error:
            annotation_router.annotate_icd_10([ICD10AnnotationRequest(id="123", text=False)])
        error_location = error.exception.errors()[0]['loc'][0]
        error_message = error.exception.errors()[0]['msg']
        assert error_location == 'text'
        assert error_message == 'text must be string and cannot be empty'

    @patch("app.util.dependency_injector.DependencyInjector.get_instance")
    def test_annotation_router__given_numeric_text_input__should_raise_validation_error(self, mock_get_instance):
        mock_get_instance.return_value = Mock()
        from app.router import annotation_router
        with self.assertRaises(ValidationError) as error:
            annotation_router.annotate_icd_10([ICD10AnnotationRequest(id="123", text="1.12")])
        error_location = error.exception.errors()[0]['loc'][0]
        error_message = error.exception.errors()[0]['msg']
        assert error_location == 'text'
        assert error_message == 'text must be string and cannot be empty'

        with self.assertRaises(ValidationError) as error:
            annotation_router.annotate_icd_10([ICD10AnnotationRequest(id="123", text=111)])
        error_location = error.exception.errors()[0]['loc'][0]
        error_message = error.exception.errors()[0]['msg']
        assert error_location == 'text'
        assert error_message == 'text must be string and cannot be empty'

    @patch("app.util.dependency_injector.DependencyInjector.get_instance")
    def test_annotation_router__given_boolean_id__input__should_raise_validation_error(self, mock_get_instance):
        mock_get_instance.return_value = Mock()
        from app.router import annotation_router
        with self.assertRaises(ValidationError) as error:
            annotation_router.annotate_icd_10([ICD10AnnotationRequest(id="true", text="1.12")])
        error_location = error.exception.errors()[0]['loc'][0]
        error_message = error.exception.errors()[0]['msg']
        assert error_location == 'id'
        assert error_message == 'id must be string and cannot be empty'

        with self.assertRaises(ValidationError) as error:
            annotation_router.annotate_icd_10([ICD10AnnotationRequest(id="true", text=111)])
        error_location = error.exception.errors()[0]['loc'][0]
        error_message = error.exception.errors()[0]['msg']
        assert error_location == 'id'
        assert error_message == 'id must be string and cannot be empty'
