from unittest import TestCase
from unittest.mock import patch

from requests import RequestException

from app.dto.request.external_api_post_request_dto import ExternalApiPostRequestDto
from app.dto.response.external_api_response_dto import ExternalApiResponseDto
from app.service.impl.external_api_service_impl import ExternalApiServiceImpl


class MockedGetResponseObject:
    def __init__(self, response: []):
        self.response = response

    def json(self):
        return self.response


class MockedPostResponseObject:
    def __init__(self, response: dict):
        self.response = response

    def json(self):
        return self.response


def mock_rest_client_util_get_posts(url):
    response = [
        {"userId": "1",
         "id": "1",
         "title": "title1",
         "body": "body1"},

        {"userId": "2",
         "id": "2",
         "title": "title2",
         "body": "body2"}
    ]
    mocked_obj = MockedGetResponseObject(response)
    return mocked_obj


def mock_rest_client_util_get_posts_for_exception(url):
    raise RequestException("This is a request exception")


def mock_rest_client_util_create_posts(url, req_dto):
    response = {"userId": "1",
                "id": "1",
                "title": "title1",
                "body": "body1"}
    mocked_obj = MockedPostResponseObject(response)
    return mocked_obj


class TestIExternalApiServiceImpl(TestCase):
    service: ExternalApiServiceImpl = ExternalApiServiceImpl()

    @patch("app.util.rest_client_util.RestClientUtil.get_sync", mock_rest_client_util_get_posts)
    def test_external_api_service_get_posts_should_return_correct_response(self):
        response = self.service.get_posts()
        assert len(response) == 2

    @patch("app.util.rest_client_util.RestClientUtil.post_sync", mock_rest_client_util_create_posts)
    def test_external_api_service_create_posts_should_return_correct_response(self):
        req_dto = ExternalApiPostRequestDto(user_id="1", title="title1", body="body1")
        response = self.service.create_posts(req_dto)
        assert response.id == "1"
        assert response.user_id == "1"
        assert response.title == "title1"
        assert response.body == "body1"
        assert type(response) == ExternalApiResponseDto

    @patch("app.util.rest_client_util.RestClientUtil.get_sync", mock_rest_client_util_get_posts_for_exception)
    def test_external_api_service_when_throws_request_exception_should_return_correct_response(self):
        with self.assertRaises(RequestException) as raisedException:
            self.service.get_posts()
        assert raisedException.exception.args[0] == "This is a request exception"
