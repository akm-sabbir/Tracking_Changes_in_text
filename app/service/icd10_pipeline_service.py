from abc import ABC, abstractmethod

from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult


class ICD10PipelineService(ABC):

    @abstractmethod
    def run_icd10_pipeline(self, text: str) -> BasePipelineComponentResult:
        raise NotImplementedError()
