from fastapi import APIRouter
from typing import List

from app.dto.request.external_api_post_request_dto import ExternalApiPostRequestDto
from app.dto.response.external_api_response_dto import ExternalApiResponseDto
from app.service.external_api_service import ExternalApiService
from app.service.impl.external_api_service_impl import ExternalApiServiceImpl
from app.util.dependency_injector import DependencyInjector

router = APIRouter()
prefix = "/externalApi"
__external_api_service: ExternalApiService = DependencyInjector.get_instance(ExternalApiServiceImpl)


@router.get("/")
async def external_api_message() -> dict:
    return {"text": "This url calls an external Api."}


@router.get(path="/posts", response_model=List[ExternalApiResponseDto], status_code=200)
async def get_posts():
    result = __external_api_service.get_posts()
    return result


@router.post(path="/posts", response_model=ExternalApiResponseDto, status_code=200)
async def create_posts(req_dto: ExternalApiPostRequestDto):
    result = __external_api_service.create_posts(req_dto)
    return result
