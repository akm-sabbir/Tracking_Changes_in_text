from abc import abstractmethod, ABC
from typing import List


class ICD10AnnotatorServiceWithFilter(ABC):
    @abstractmethod
    def get_icd_10_filtered_codes(self, text: str) -> List:
        raise NotImplementedError()
