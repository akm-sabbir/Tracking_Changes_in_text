import asyncio
from asyncio import AbstractEventLoop
from unittest import TestCase
from unittest.mock import patch

from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper, ValidationError

from app.dto.request.hcc_request_dto import HCCRequestDto
from app.router import hcc_router
from app.dto.response.hcc_response_dto import HCCResponseDto


def get_mocked_request_validation_error(req_dto: HCCRequestDto):
    validation_errors = [ErrorWrapper(exc=Exception(), loc=("orec",))]
    raise RequestValidationError(errors=[
        ErrorWrapper(exc=ValidationError(model=HCCRequestDto, errors=validation_errors),
                     loc=('body',), )], body={'', })


class MockedHCCService:
    def get_hcc_risk_scores(self, request_dto: HCCRequestDto) -> HCCResponseDto:
        response = HCCResponseDto(hcc_maps={"I5030": "HCC85"}, hcc_scores={"CND_HCC85": 0.404},
                                  demographics_score={}, disease_interactions_score={"CHF_Diabetes": 0.33},
                                  aggregated_risk_score=1.82, demographics_details={})
        return response


class TestHCCRouter(TestCase):
    __loop: AbstractEventLoop

    @classmethod
    def setUpClass(cls):
        cls.__loop = asyncio.new_event_loop()

    @classmethod
    def tearDownClass(cls):
        cls.__loop.close()

    @patch.object(hcc_router, "__hcc_service", MockedHCCService())
    def test_hcc_api_message__should_return_correct_output(self):
        response = self.__loop.run_until_complete(hcc_router.hcc_api_message())
        assert response["text"] == "This is HCC Risk Score Calculator."

    @patch.object(hcc_router, "__hcc_service", MockedHCCService())
    def test_get_hcc_risk_scores__given_correct_input__should_return_correct_output(self):
        req_dto = HCCRequestDto(icd_codes_list=["code1", "code2"])
        response = self.__loop.run_until_complete(hcc_router.calculate_hcc_scores(req_dto))
        assert response.hcc_maps == {'I5030': 'HCC85'}
        assert response.hcc_scores == {'CND_HCC85': 0.404}
        assert response.demographics_score == {}
        assert response.disease_interactions_score == {'CHF_Diabetes': 0.33}
        assert response.aggregated_risk_score == 1.82
        assert response.demographics_details == {}

    @patch("app.router.hcc_router.__hcc_service.get_hcc_risk_scores", get_mocked_request_validation_error)
    def test_hcc_router_when_throws_request_validation_error_should_return_correct_output(self):
        req_dto = HCCRequestDto(icd_codes_list=["code1", "code2"], orec="A")
        with self.assertRaises(RequestValidationError) as raisedException:
            self.__loop.run_until_complete(hcc_router.calculate_hcc_scores(req_dto))
        assert raisedException.exception.errors() == [
            {'loc': ('body', 'orec'), 'msg': '', 'type': 'value_error.exception'}]
