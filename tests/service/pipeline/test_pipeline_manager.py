from unittest import TestCase

from app.exception.service_exception import ServiceException
from app.service.pipeline.components.dummy_component_one import DummyComponentOne
from app.service.pipeline.components.dummy_component_three import DummyComponentThree
from app.service.pipeline.components.dummy_component_two import DummyComponentTwo
from app.service.pipeline.pipeline_manager import PipelineManager


class TestPipelineManager(TestCase):

    def test__run_pipeline__should_return_correct_response__given_correct_components(self):
        pipeline_components = [DummyComponentOne(), DummyComponentTwo(), DummyComponentThree()]
        pipeline_result = PipelineManager(pipeline_components).run_pipeline({})
        assert pipeline_result[DummyComponentOne][0].message == "dummy"
        assert pipeline_result[DummyComponentTwo][0].message == "dummy two"
        assert pipeline_result[DummyComponentThree][0].message == "dummy three"

    def test__run_pipeline__should_raise_exception__given_dependencies_not_added(self):
        with self.assertRaises(ServiceException) as error:
            pipeline_components = [DummyComponentTwo(), DummyComponentThree()]
            PipelineManager(pipeline_components).run_pipeline({})
        assert str(error.exception) == "Dependencies of " + DummyComponentTwo.__name__ + " not satisfied"
