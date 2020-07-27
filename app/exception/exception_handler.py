from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from requests import RequestException

from app.exception.error_response_factory import ErrorResponseFactory
from app.exception.service_exception import ServiceException


class ExceptionHandler:

    @staticmethod
    async def __validation_exception_handler(request: Request, exception: RequestValidationError):
        return ErrorResponseFactory.get_validation_error_response(exception)

    @staticmethod
    async def __service_exception_handler(request: Request, exception: ServiceException):
        return ErrorResponseFactory.get_error_response(exception, exception.status, exception.message)

    @staticmethod
    async def __request_exception_handler(request: Request, exception: RequestException):
        return ErrorResponseFactory.get_generic_error_response(exception)

    @classmethod
    def initiate_exception_handlers(cls, app: FastAPI):
        app.add_exception_handler(exc_class_or_status_code=RequestValidationError,

                                  handler=cls.__validation_exception_handler)
        app.add_exception_handler(exc_class_or_status_code=ServiceException,

                                  handler=cls.__service_exception_handler)
        app.add_exception_handler(exc_class_or_status_code=RequestException,
                                  handler=cls.__request_exception_handler)
