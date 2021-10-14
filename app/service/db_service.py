from abc import ABC, abstractmethod
from typing import Any


class DBService(ABC):

    @abstractmethod
    def get_item(self, item_id: Any):
        pass

    @abstractmethod
    def save_item(self, model: Any):
        pass
