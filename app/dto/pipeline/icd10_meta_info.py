from dataclasses import dataclass
from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


@dataclass
class icd10_meta_info(BasePipelineComponentResult):
    hcc_map: str = ''
    score: float = 0.0
    entity_score: float = 0.0
    length: int = 0
    remove: bool = False
