from abc import ABC, abstractmethod
from typing import List


class RxNormAnnotatorService(ABC):
    @abstractmethod
    def get_rxnorm_codes(self, text: str) -> List:
        raise NotImplementedError()
