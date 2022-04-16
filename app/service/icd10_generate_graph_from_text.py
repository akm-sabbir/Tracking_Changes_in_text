from abc import ABC, abstractmethod


class ICD10GenerateGraphFromText(ABC):
    @abstractmethod
    def process_token_to_create_graph(self, spanned_info: list) -> dict:
        raise NotImplementedError()
