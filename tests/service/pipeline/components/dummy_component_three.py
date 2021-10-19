from typing import List

from app.dto.pipeline.dummy_component_three_result import DummyComponentThreeResult
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from tests.service.pipeline.components.dummy_component_one import DummyComponentOne
from tests.service.pipeline.components.dummy_component_two import DummyComponentTwo


class DummyComponentThree(BasePipelineComponent):
    DEPENDS_ON: List = [DummyComponentOne, DummyComponentTwo]

    def run(self, annotation_results: dict) -> List[DummyComponentThreeResult]:
        return [DummyComponentThreeResult("dummy three")]
