from abc import ABC
from app.dto.request.hcc_request_dto import  HCCRequestDto
from app.dto.response.hcc_response_dto import HCCResponseDto


class HCCService(ABC):
    def get_hcc_risk_scores(self, hcc_request_dto: HCCRequestDto) -> HCCResponseDto:
        raise NotImplementedError()