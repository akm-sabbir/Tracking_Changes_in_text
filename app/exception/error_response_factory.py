import logging
from datetime import datetime
from http import HTTPStatus

from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response
from typing import List, Dict

from app.exception.error_response import ErrorResponse


def get_datetime_now():
    return datetime.now()


class ErrorResponseFactory:
    __logger = logging.getLogger(__name__)
    __INTERNAL_SERVER_ERROR_MESSAGE = "Something went wrong. Please try again after sometime."

    @staticmethod
    def get_error_response(ex: Exception, status_code: HTTPStatus, client_message: str) -> Response:
        ErrorResponseFactory.__logger.error("An exception occurred", exc_info=True)
        error_response = ErrorResponse(
            timestamp=str(get_datetime_now()),
            status=status_code.value,
            error=status_code.phrase,
            message=client_message)
        return Response(error_response.json(), media_type="application/json", status_code=status_code.value)

    @staticmethod
    def get_generic_error_response(exception: Exception) -> Response:
        return ErrorResponseFactory.get_error_response(exception, HTTPStatus.INTERNAL_SERVER_ERROR,
                                                       ErrorResponseFactory.__INTERNAL_SERVER_ERROR_MESSAGE)

    @staticmethod
    def get_validation_error_response(exception: RequestValidationError) -> Response:
        return ErrorResponseFactory.get_error_response(exception,
                                                       HTTPStatus.BAD_REQUEST,
                                                       ErrorResponseFactory.get_request_validation_error_msg(
                                                           exception.errors())
                                                       )

    @staticmethod
    def get_request_validation_error_msg(errors: List[Dict]):
        msg: str = ",".join([str(error['loc'][1]) + ":" + str(error['msg']) for error in errors])
        return msg

