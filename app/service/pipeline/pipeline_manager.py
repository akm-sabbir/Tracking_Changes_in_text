from typing import List, NoReturn

from app.exception.service_exception import ServiceException
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent


class PipelineManager:
    def __init__(self, pipeline_components: List[BasePipelineComponent]):
        self.__pipeline_components = pipeline_components
        self.__check_dependencies()

    def run_pipeline(self, **initial_input) -> dict:
        annotation_results: dict = initial_input
        for component in self.__pipeline_components:
            annotation_results[component.__class__] = component.run(annotation_results)
        return annotation_results

    def __check_dependencies(self) -> NoReturn:
        component_presence_map = set()
        for component in self.__pipeline_components:
            if set(component.DEPENDS_ON).intersection(component_presence_map) != set(component.DEPENDS_ON):
                raise ServiceException("Dependencies of " + component.__class__.__name__ + " not satisfied")
            else:
                component_presence_map.add(component.__class__)
