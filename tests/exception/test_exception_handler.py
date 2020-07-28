from unittest import TestCase

from fastapi import FastAPI

from app.exception.exception_handler import ExceptionHandler


class TestExceptionHandler(TestCase):
    def test_initiate_exception_handlers_should_return_added_exception_handlers(self):
        app = FastAPI()
        ExceptionHandler.initiate_exception_handlers(app)
        assert len(app.exception_handlers) == 4