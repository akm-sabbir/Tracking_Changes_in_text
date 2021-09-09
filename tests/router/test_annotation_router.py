import asyncio
from asyncio import AbstractEventLoop
from unittest import TestCase
from unittest.mock import Mock, patch

from pydantic import ValidationError

from app.dto.request.icd10_annotation_request import ICD10AnnotationRequest
from app.dto.response.icd10_annotation_response import ICD10AnnotationResponse
from app.router import annotation_router


class Test(TestCase):
    __loop: AbstractEventLoop

    @classmethod
    def setUpClass(cls):
        cls.__loop = asyncio.new_event_loop()

    @classmethod
    def tearDownClass(cls):
        cls.__loop.close()

    @patch.object(annotation_router, "__icd10_service")
    def test__annotation_router__given_correct_input__should_return_correct_response(self, mock_icd10_service: Mock):
        mock_icd10_service.annotate_icd_10 = Mock()
        mock_icd10_service.annotate_icd_10.return_value = ICD10AnnotationResponse(icd10_annotations=["a", "b", "c"])
        response = self.__loop.run_until_complete(
            annotation_router.annotate_icd_10(ICD10AnnotationRequest(text="text")))
        assert response.icd10_annotations == ["a", "b", "c"]
        mock_icd10_service.annotate_icd_10.assert_called_once_with("text")

    def test_annotation_router__given_boolean_input__should_raise_validation_error(self):
        with self.assertRaises(ValidationError) as error:
            annotation_router.annotate_icd_10(ICD10AnnotationRequest(text="true"))
        error_location = error.exception.errors()[0]['loc'][0]
        error_message = error.exception.errors()[0]['msg']
        assert error_location == 'text'
        assert error_message == 'must be string and cannot be empty'

        with self.assertRaises(ValidationError) as error:
            annotation_router.annotate_icd_10(ICD10AnnotationRequest(text=False))
        error_location = error.exception.errors()[0]['loc'][0]
        error_message = error.exception.errors()[0]['msg']
        assert error_location == 'text'
        assert error_message == 'must be string and cannot be empty'

    def test_annotation_router__given_numeric_input__should_raise_validation_error(self):
        with self.assertRaises(ValidationError) as error:
            annotation_router.annotate_icd_10(ICD10AnnotationRequest(text="1.12"))
        error_location = error.exception.errors()[0]['loc'][0]
        error_message = error.exception.errors()[0]['msg']
        assert error_location == 'text'
        assert error_message == 'must be string and cannot be empty'

        with self.assertRaises(ValidationError) as error:
            annotation_router.annotate_icd_10(ICD10AnnotationRequest(text=111))
        error_location = error.exception.errors()[0]['loc'][0]
        error_message = error.exception.errors()[0]['msg']
        assert error_location == 'text'
        assert error_message == 'must be string and cannot be empty'


