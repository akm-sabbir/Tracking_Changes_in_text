from fastapi import APIRouter
from app.service.hcc_service import HCCService
from app.service.impl.hcc_service_impl import HCCCServiceImpl
from app.dto.request.hcc_request_dto import HCCRequestDto
from app.util.dependency_injector import DependencyInjector
from app.dto.response.hcc_response_dto import HCCResponseDto

router = APIRouter()
prefix = "/hcc"
__hcc_service: HCCService = DependencyInjector.get_instance(HCCCServiceImpl)


@router.get("/")
async def hcc_api_message() -> dict:
    return {"text": "This is HCC Risk Score Calculator."}


@router.post(path="/risk-scores", response_model=HCCResponseDto, status_code=200)
async def calculate_hcc_scores(req_dto: HCCRequestDto) -> HCCResponseDto:
    result = __hcc_service.get_hcc_risk_scores(req_dto)
    return result
