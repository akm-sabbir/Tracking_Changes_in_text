from dataclasses import dataclass
from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.dto.pipeline.icd10_meta_info import ICD10MetaInfo

@dataclass
class Icd10HccMeta(BasePipelineComponentResult):
    hcc_annotation_response: HCCResponseDto = None
    hcc_meta_map_info: ICD10MetaInfo = None