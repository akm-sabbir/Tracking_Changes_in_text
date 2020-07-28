import asyncio
from asyncio import AbstractEventLoop
from http import HTTPStatus
from unittest import TestCase
from unittest.mock import patch
from typing import List
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from requests import RequestException

from app.dto.request.external_api_post_request_dto import ExternalApiPostRequestDto
from app.exception.service_exception import ServiceException
from app.router import external_api_router

from app.dto.response.external_api_response_dto import ExternalApiResponseDto


def get_mocked_request_validation_error(req_dto: ExternalApiPostRequestDto):
    validation_errors = [ErrorWrapper(exc=Exception(), loc=("userId",))]
    raise RequestValidationError(errors=[
        ErrorWrapper(exc=ValidationError(model=ExternalApiPostRequestDto, errors=validation_errors),
                     loc=('body',), )], body={'', })


def get_mocked_service_exception():
    raise ServiceException()


def get_mocked_request_exception():
    raise RequestException('This is a request exception')


class MockedExternalApiService:

    def get_posts(self) -> List[ExternalApiResponseDto]:
        response = [ExternalApiResponseDto(id="1", user_id="1", title="mocked_title", body="body1")]
        return response

    def create_posts(self, req_dto: ExternalApiPostRequestDto) -> ExternalApiResponseDto:
        response = ExternalApiResponseDto(id="1", user_id="1", title="new_title", body="body1")
        return response


class TestExternalApiRouter(TestCase):
    __loop: AbstractEventLoop

    @classmethod
    def setUpClass(cls):
        cls.__loop = asyncio.new_event_loop()

    @classmethod
    def tearDownClass(cls):
        cls.__loop.close()

    @patch.object(external_api_router, "__external_api_service", MockedExternalApiService())
    def test_external_api_message_should_return_correct_output(self):
        response = self.__loop.run_until_complete(external_api_router.external_api_message())
        assert response["text"] == "This url calls an external Api."

    @patch.object(external_api_router, "__external_api_service", MockedExternalApiService())
    def test_get_posts_should_return_correct_output(self):
        response = self.__loop.run_until_complete(external_api_router.get_posts())
        assert len(response) == 1
        assert response[0].user_id == "1"
        assert response[0].id == "1"
        assert response[0].title == "mocked_title"
        assert response[0].body == "body1"

    @patch.object(external_api_router, "__external_api_service", MockedExternalApiService())
    def test_create_posts_should_return_correct_output(self):
        req_dto = ExternalApiPostRequestDto(user_id="1", title="title1", body="body1")
        response = self.__loop.run_until_complete(external_api_router.create_posts(req_dto))
        assert response.user_id == "1"
        assert response.id == "1"
        assert response.title == "new_title"
        assert response.body == "body1"

    @patch("app.router.external_api_router.__external_api_service.create_posts", get_mocked_request_validation_error)
    def test_create_posts_when_throws_validation_error_should_return_correct_output(self):
        req_dto = ExternalApiPostRequestDto(title="title", userId="userId", body="body")
        with self.assertRaises(RequestValidationError) as raisedException:
            self.__loop.run_until_complete(external_api_router.create_posts(req_dto))
        assert raisedException.exception.errors() == [
            {'loc': ('body', 'userId'), 'msg': '', 'type': 'value_error.exception'}]

    @patch("app.router.external_api_router.__external_api_service.get_posts", get_mocked_service_exception)
    def test_external_api_service_when_throws_service_exception_should_return_correct_output(self):
        with self.assertRaises(ServiceException) as raisedException:
            self.__loop.run_until_complete(external_api_router.get_posts())
        assert raisedException.exception.status == HTTPStatus.INTERNAL_SERVER_ERROR
        assert raisedException.exception.message == "Something went wrong. Please try again after sometime."

    @patch("app.router.external_api_router.__external_api_service.get_posts", get_mocked_request_exception)
    def test_external_api_service_router_when_throws_request_exception_should_return_correct_output(self):
        with self.assertRaises(RequestException) as raisedException:
            self.__loop.run_until_complete(external_api_router.get_posts())
        assert raisedException.exception.args[0] == 'This is a request exception'
