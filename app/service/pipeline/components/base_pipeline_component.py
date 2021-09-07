from abc import ABC, abstractmethod
from typing import List

from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult
from app.exception.service_exception import ServiceException


class BasePipelineComponent(ABC):
    DEPENDS_ON: List = [None]

    def __init__(self):
        if self.DEPENDS_ON == [None]:
            raise ServiceException(
                "Please define DEPENDS_ON (it can be []) for annotator " + self.__class__.__name__)

    @abstractmethod
    def run(self, annotation_results: dict) -> List[BasePipelineComponentResult]:
        pass
