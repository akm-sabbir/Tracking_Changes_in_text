from abc import ABC, abstractmethod


class ICD10ChangeInTextStructure(ABC):
    @abstractmethod
    def generate_metainfo_for_changed_text(self, spanned_info: dict) -> dict:
        raise NotImplementedError()
