from abc import ABC
from typing import List

from app.dto.request.external_api_post_request_dto import ExternalApiPostRequestDto
from app.dto.response.external_api_response_dto import ExternalApiResponseDto


class ExternalApiService(ABC):

    def get_posts(self) -> List[ExternalApiResponseDto]:
        raise NotImplementedError()

    def create_posts(self, request_dto: ExternalApiPostRequestDto) -> ExternalApiResponseDto:
        raise NotImplementedError()

