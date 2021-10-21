from typing import List

from app.dto.pipeline.dummy_component_four_result import DummyComponentFourResult
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from tests.service.pipeline.components.dummy_component_one import DummyComponentOne
from tests.service.pipeline.components.dummy_component_two import DummyComponentTwo
from tests.service.pipeline.components.dummy_component_three import  DummyComponentThree


class DummyComponentFour(BasePipelineComponent):
    DEPENDS_ON: List = [DummyComponentOne, DummyComponentTwo, DummyComponentThree]

    def run(self, annotation_results: dict) -> List[DummyComponentFourResult]:
        return [DummyComponentFourResult("dummy four")]
