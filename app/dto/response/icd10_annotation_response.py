from typing import List, Dict

from app.dto.base_dto import BaseDto
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.response.hcc_response_dto import HCCResponseDto


class ICD10AnnotationResponse(BaseDto):
    id: str
    icd10_annotations: List[ICD10AnnotationResult]
    raw_acm_data: List[Dict]
    hcc_maps: HCCResponseDto
    is_smoker: bool
