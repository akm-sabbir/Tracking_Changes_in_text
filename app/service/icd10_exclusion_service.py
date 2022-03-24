
from abc import abstractmethod, ABC
from typing import List


class ICD10ExclusionService(ABC):
    @abstractmethod
    def get_icd10_code_exclusion_decision_based_graph(self, icd_data_dict: dict) -> str:
        raise NotImplementedError()