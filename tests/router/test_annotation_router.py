import asyncio
from asyncio import AbstractEventLoop
from unittest import TestCase
from unittest.mock import Mock, patch

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
    def test_health_check(self, mock_icd10_service: Mock):
        mock_icd10_service.annotate_icd_10 = Mock()
        mock_icd10_service.annotate_icd_10.return_value = ICD10AnnotationResponse(icd10_annotations=["a", "b", "c"])
        response = self.__loop.run_until_complete(
            annotation_router.annotate_icd_10(ICD10AnnotationRequest(text="text")))
        assert response.icd10_annotations == ["a", "b", "c"]
        mock_icd10_service.annotate_icd_10.assert_called_once_with("text")
