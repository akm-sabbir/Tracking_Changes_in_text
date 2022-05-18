from typing import Dict, List

from app.dto.base_dto import BaseDto
from app.dto.core.service.hcc_code import HCCCode
from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class HCCResponseDto(BasePipelineComponentResult, BaseDto):
    hcc_maps: Dict[str, HCCCode]
    demographics_score: dict
    disease_interactions_score: dict
    aggregated_risk_score: float
    demographics_details: dict
    hcc_categories: dict
    default_selection: List[str]
