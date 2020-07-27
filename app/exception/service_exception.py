from http import HTTPStatus


class ServiceException(Exception):
    def __init__(self, status=HTTPStatus.INTERNAL_SERVER_ERROR,
                 message="Something went wrong. Please try again after sometime."):
        self.status = status
        self.message = message
