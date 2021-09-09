from cgitb import text
from unittest import TestCase
from unittest.mock import patch, Mock

from app.dto.pipeline.dummy_component_one_result import DummyComponentOneResult
from app.dto.pipeline.dummy_component_three_result import DummyComponentThreeResult
from app.dto.pipeline.dummy_component_two_result import DummyComponentTwoResult
from app.dto.response.icd10_annotation_response import ICD10AnnotationResponse
from app.service.impl.icd10_annotator_service_impl import ICD10AnnotatorServiceImpl
from app.service.pipeline.components.dummy_component_one import DummyComponentOne
from app.service.pipeline.components.dummy_component_three import DummyComponentThree
from app.service.pipeline.components.dummy_component_two import DummyComponentTwo


class TestICD10AnnotatorServiceImpl(TestCase):

    def test__annotate_icd_10__should_return_correct_response__given_correct_input(self):
        icd10_annotator_service: ICD10AnnotatorServiceImpl = ICD10AnnotatorServiceImpl()

        mock_run_pipeline = Mock()
        mock_run_pipeline.return_value = {DummyComponentOne: DummyComponentOneResult("a"),
                                          DummyComponentTwo: DummyComponentTwoResult("b"),
                                          DummyComponentThree: DummyComponentThreeResult("c")}

        icd10_annotator_service._ICD10AnnotatorServiceImpl__pipeline_manager = Mock()
        icd10_annotator_service._ICD10AnnotatorServiceImpl__pipeline_manager.run_pipeline = mock_run_pipeline
        response: ICD10AnnotationResponse = icd10_annotator_service.annotate_icd_10(text="text")
        assert response.icd10_annotations[0].message == "a"
        assert response.icd10_annotations[1].message == "b"
        assert response.icd10_annotations[2].message == "c"
        mock_run_pipeline.assert_called_once_with(text='text')
