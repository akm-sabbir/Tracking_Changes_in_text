from unittest import TestCase

from app.exception.service_exception import ServiceException
from app.service.pipeline.components.dummy_component import DummyComponent
from app.service.pipeline.components.dummy_component_three import DummyComponentThree
from app.service.pipeline.components.dummy_component_two import DummyComponentTwo
from app.service.pipeline.pipeline_manager import PipelineManager


class TestPipelineManager(TestCase):

    def test__run_pipeline__should_return_correct_response__given_correct_components(self):
        pipeline_components = [DummyComponentTwo(), DummyComponentThree(), DummyComponent()]
        pipeline_result = PipelineManager(pipeline_components).run_pipeline()
        assert pipeline_result[DummyComponent.ANNOTATION_LABEL_NAME][0].message == "dummy"
        assert pipeline_result[DummyComponentThree.ANNOTATION_LABEL_NAME][0].message == "dummy"
        assert pipeline_result[DummyComponentThree.ANNOTATION_LABEL_NAME][0].message == "dummy"

    def test__run_pipeline__should_raise_exception__given_dependencies_not_added(self):
        with self.assertRaises(ServiceException) as error:
            pipeline_components = [DummyComponentTwo(), DummyComponent()]
            PipelineManager(pipeline_components).run_pipeline()
        assert str(error.exception) == "Dependencies of " + DummyComponent.__name__ + " not satisfied"
