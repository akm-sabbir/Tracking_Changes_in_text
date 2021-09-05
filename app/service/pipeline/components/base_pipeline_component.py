from abc import ABC, abstractmethod
from typing import List

from app.dto.pipeline.base_annotation import BaseAnnotation
from app.exception.service_exception import ServiceException


class BasePipelineComponent(ABC):
    ANNOTATION_LABEL_NAME: str = ""
    DEPENDS_ON: List = None

    def __init__(self):
        if self.ANNOTATION_LABEL_NAME == "" or self.DEPENDS_ON is None:
            raise ServiceException(
                "Please define ANNOTATION_LABEL_NAME and DEPENDS_ON for annotator " + self.__class__.__name__)

    @abstractmethod
    def run(self, annotation_results: dict) -> List[BaseAnnotation]:
        pass
