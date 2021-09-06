from typing import List
from unittest import TestCase
from unittest.mock import Mock

from app.dto.pipeline.base_pipeline_component_result import BasePipelineComponentResult
from app.exception.service_exception import ServiceException
from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent


class TestBasePipelineComponent(TestCase):
    def test__init__should_raise_error__if_dependencies_not_defined(self):
        with self.assertRaises(ServiceException) as error:
            MockComponent()
        assert str(error.exception) == "Please define DEPENDS_ON for annotator " + MockComponent.__name__


class MockComponent(BasePipelineComponent):
    def run(self, annotation_results: dict) -> List[BasePipelineComponentResult]:
        pass
