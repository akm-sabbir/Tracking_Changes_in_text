from abc import ABC, abstractmethod

from app.dto.core.icd10_pipeline_params import ICD10PipelineParams
from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class ICD10PipelineService(ABC):

    @abstractmethod
    async def run_icd10_pipeline(self, params: ICD10PipelineParams) -> BasePipelineComponentResult:
        raise NotImplementedError()
