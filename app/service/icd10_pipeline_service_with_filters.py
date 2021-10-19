from abc import abstractmethod, ABC
from typing import List


class ICD10PipelineServiceWithFilter(ABC):
    @abstractmethod
    def run_icd10_pipeline(self, text: str, dx_threshold: float,
                                  icd10_threshold: float, parent_threshold: float) -> List:
        raise NotImplementedError()
