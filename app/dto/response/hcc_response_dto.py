from app.dto.base_dto import BaseDto


class HCCResponseDto(BaseDto):
    hcc_maps: dict
    hcc_scores: dict
    demographics_score: dict
    disease_interactions_score: dict
    aggregated_risk_score: float
    demographics_details: dict
