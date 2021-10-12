from abc import abstractmethod, ABC
from typing import List


class ICD10AnnotatorServiceWithFilter(ABC):
    @abstractmethod
    def get_icd_10_filtered_codes(self, text: str, dx_threshold: float,
                                  icd10_threshold: float, parent_threshold: float) -> List:
        raise NotImplementedError()
