from datetime import datetime
from http import HTTPStatus
from unittest import TestCase
from unittest.mock import patch

from fastapi.responses import Response
from app.exception.error_response_factory import ErrorResponseFactory
from app.exception.service_exception import ServiceException


def validation_exception_errors():
    validation_errors = [{'loc': ('body', 'secondNumber'),
                          "msg": "ensure this value is greater than 0",
                          "type": "value_error.number.not_gt",
                          "ctx": {"limit_value": 0}}]
    return validation_errors


class TestErrorResponseFactory(TestCase):
    @patch('app.exception.error_response_factory.ErrorResponseFactory._ErrorResponseFactory__logger')
    @patch('app.exception.error_response_factory.get_datetime_now')
    def test_get_error_response_factory_should_return_correct_response(self, mocked_datetime_now, mocked_logger):
        mocked_datetime_now.return_value = datetime(year=2020, month=6, day=30)
        response: Response = ErrorResponseFactory.get_error_response(ServiceException,
                                                                     HTTPStatus.INTERNAL_SERVER_ERROR,
                                                                     "client_message")
        self.assertTrue(mocked_logger.error.called)
        assert response.status_code == 500
        assert response.body == b'{"timestamp": "2020-06-30 00:00:00", "message": "client_message", "error":' \
                                b' "Internal Server Error", "status": 500}'

    def test_get_request_validation_error_msg_should_return_correct_response(self):
        msg: str = ErrorResponseFactory.get_request_validation_error_msg(validation_exception_errors())
        assert msg == "secondNumber:ensure this value is greater than 0"



