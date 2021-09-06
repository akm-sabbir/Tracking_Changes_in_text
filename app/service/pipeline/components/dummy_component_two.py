from typing import List

from app.dto.pipeline.dummy_component_two_result import DummyComponentTwoResult
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.pipeline.components.dummy_component_one import DummyComponentOne


class DummyComponentTwo(BasePipelineComponent):
    ANNOTATION_LABEL_NAME: str = "dummy_one"
    DEPENDS_ON: List = [DummyComponentOne]

    def run(self, annotation_results: dict) -> List[DummyComponentTwoResult]:
        return [DummyComponentTwoResult("dummy two")]
