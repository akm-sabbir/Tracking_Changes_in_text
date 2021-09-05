from typing import List

from app.dto.pipeline.dummy_annotation import DummyAnnotation
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.dummy_component_two import DummyComponentTwo
from app.service.pipeline.components.dummy_component_three import DummyComponentThree


class DummyComponent(BasePipelineComponent):
    ANNOTATION_LABEL_NAME: str = "dummy_one"
    DEPENDS_ON: List = [DummyComponentTwo, DummyComponentThree]

    def run(self, annotation_results: dict) -> List[DummyAnnotation]:
        return [DummyAnnotation("dummy")]
