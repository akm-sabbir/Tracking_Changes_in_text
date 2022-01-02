from dataclasses import dataclass
from typing import Dict

from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult
from app.dto.pipeline.icd10_meta_info import ICD10MetaInfo
from app.dto.response.hcc_response_dto import HCCResponseDto


@dataclass
class Icd10HccMeta(BasePipelineComponentResult):
    def __init__(self, hcc_annotation_response: HCCResponseDto, hcc_meta_map_info: Dict[str, ICD10MetaInfo]):
        self.hcc_annotation_response = hcc_annotation_response
        self.hcc_meta_map_info = hcc_meta_map_info
