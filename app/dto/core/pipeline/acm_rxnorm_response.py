from typing import List, Dict

from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult
from app.dto.pipeline.rxnorm_annotation_result import RxNormAnnotationResult


class ACMRxNormResult(BasePipelineComponentResult):
    def __init__(self, note_id: str, rxnorm_annotations: List[RxNormAnnotationResult], raw_acm_data: List[Dict]):
        self.id: str = note_id
        self.rxnorm_annotations: List[RxNormAnnotationResult] = rxnorm_annotations
        self.raw_acm_data: List[Dict] = raw_acm_data
        