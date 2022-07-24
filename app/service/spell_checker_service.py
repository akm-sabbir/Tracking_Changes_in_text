from abc import ABC, abstractmethod


class SpellCheckerService(ABC):
    @abstractmethod
    def get_corrected_text(self, sentence: str) -> str:
        raise NotImplementedError()
