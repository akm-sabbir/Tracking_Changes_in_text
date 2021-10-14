from typing import Dict

from app.dto.base_dto import BaseDto
from app.dto.core.service.hcc_code import HCCCode


class HCCResponseDto(BaseDto):
    hcc_maps: Dict[str, HCCCode]
    demographics_score: dict
    disease_interactions_score: dict
    aggregated_risk_score: float
    demographics_details: dict
