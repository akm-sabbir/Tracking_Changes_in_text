from abc import ABC, abstractmethod


class ICD10TextTokenAndSpanGeneration(ABC):
    @abstractmethod
    def get_token_with_span(self, text: str) -> list:
        raise NotImplementedError()
