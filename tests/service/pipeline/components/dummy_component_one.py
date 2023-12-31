from typing import List

from app.dto.pipeline.dummy_component_one_result import DummyComponentOneResult
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent


class DummyComponentOne(BasePipelineComponent):
    DEPENDS_ON: List = []

    def run(self, annotation_results: dict) -> List[DummyComponentOneResult]:
        return [DummyComponentOneResult(annotation_results['text'])]
