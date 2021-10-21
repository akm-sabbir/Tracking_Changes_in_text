from abc import abstractmethod, ABC
from typing import List


class ICD10AnnotatorServiceWithFilters(ABC):
    @abstractmethod
    def get_icd_10_filtered_codes(self, text: str, hcc_map: dict, dx_threshold: float,
                                  icd10_threshold: float, parent_threshold: float) -> List:
        raise NotImplementedError()
