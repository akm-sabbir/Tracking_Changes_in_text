from typing import List

from app.dto.pipeline.dummy_annotation_three import DummyAnnotationThree
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.dummy_component_two import DummyComponentTwo


class DummyComponentThree(BasePipelineComponent):
    ANNOTATION_LABEL_NAME: str = "dummy_one"
    DEPENDS_ON: List = [DummyComponentTwo]

    def run(self, annotation_results: dict) -> List[DummyAnnotationThree]:
        return [DummyAnnotationThree("dummy three")]