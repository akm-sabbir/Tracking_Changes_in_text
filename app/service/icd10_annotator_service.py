from abc import abstractmethod, ABC
from typing import List


class ICD10AnnotatorService(ABC):
    @abstractmethod
    def get_icd_10_codes(self, text: str) -> List:
        raise NotImplementedError()
