
from abc import abstractmethod, ABC
from typing import List


class ICD10ExclusionService(ABC):
    @abstractmethod
    def get_icd_10_code_exclusion_decision(self, icd_data_dict: dict) -> str:
        raise NotImplementedError()