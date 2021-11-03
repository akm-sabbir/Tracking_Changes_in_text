
from abc import abstractmethod, ABC
from typing import List


class ICD10NegationService(ABC):
    @abstractmethod
    def get_icd_10_text_negation_fixed(self, text: str) -> str:
        raise NotImplementedError()