import logging
from typing import List

from injector import singleton

from app.dto.request.external_api_post_request_dto import ExternalApiPostRequestDto
from app.dto.response.external_api_response_dto import ExternalApiResponseDto
from app.service.external_api_service import ExternalApiService
from app.util.rest_client_util import RestClientUtil


@singleton
class ExternalApiServiceImpl(ExternalApiService):
    __logger = logging.getLogger(__name__)

    def get_posts(self) -> List[ExternalApiResponseDto]:
        url: str = "https://jsonplaceholder.typicode.com/posts"
        self.__create_log(url, "get")
        response = RestClientUtil.get_sync(url)
        posts = [ExternalApiResponseDto(**obj_dict) for obj_dict in response.json()]
        return posts

    def create_posts(self, req_dto: ExternalApiPostRequestDto) -> ExternalApiResponseDto:
        url: str = "https://jsonplaceholder.typicode.com/posts"
        self.__create_log(url, "post")
        dto_dict = vars(req_dto)
        response = RestClientUtil.post_sync(url=url, req_dto=dto_dict)
        return ExternalApiResponseDto(**response.json())

    def __create_log(self, url: str, operation: str):
        self.__logger.debug(
            "Performing : " + operation + " request at url " + url)
