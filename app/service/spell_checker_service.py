from abc import ABC, abstractmethod


class SpellCheckerService(ABC):
    @abstractmethod
    def get_corrected_text(self, sentence: str, max_edit_distance: int, transfer_casing: bool, ignore_non_words: bool,
                           split_by_space: bool, ignore_term_with_digits: bool) -> str:
        raise NotImplementedError()
