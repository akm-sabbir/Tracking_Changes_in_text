from unittest import TestCase
from unittest.mock import Mock, patch

from app.dto.core.pipeline.acm_icd10_response import ACMICD10Result
from app.dto.pipeline.dummy_component_one_result import DummyComponentOneResult
from app.dto.pipeline.dummy_component_two_result import DummyComponentTwoResult
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.response.icd10_annotation_response import ICD10AnnotationResponse
from app.service.impl.icd10_pipeline_service_impl import ICD10PipelineServiceImpl
from app.service.pipeline.components.acm_icd10_annotation_component import ACMICD10AnnotationComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from service.pipeline.components.dummy_component_one import DummyComponentOne
from service.pipeline.components.dummy_component_two import DummyComponentTwo


class TestICD10PipelineServiceImpl(TestCase):

    @patch("app.service.impl.amazon_icd10_annotator_service.boto3", Mock())
    @patch("app.service.impl.dynamo_db_service.boto3", Mock())
    @patch("app.util.config_manager.ConfigManager.get_specific_config")
    def test__annotate_icd_10__should_return_correct_response__given_correct_input(self,
                                                                                   mock_get_config: Mock):
        mock_get_config.return_value = "table_name"
        icd10_annotation_1 = ICD10Annotation(code="A15.0", description="Tuberculosis of lung", score=0.7)
        icd10_annotation_2 = ICD10Annotation(code="A15.9", description="Respiratory tuberculosis unspecified",
                                             score=0.54)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=12,
                                                          end_offset=24, is_negated=False,
                                                          suggested_codes=[icd10_annotation_1, icd10_annotation_2],
                                                          raw_acm_response={"data": "data1"})

        icd10_annotator_service: ICD10PipelineServiceImpl = ICD10PipelineServiceImpl()

        mock_run_pipeline = Mock()
        mock_run_pipeline.return_value = {DummyComponentOne: [DummyComponentOneResult("a")],
                                          DummyComponentTwo: [DummyComponentTwoResult("b")],
                                          ACMICD10AnnotationComponent: [ACMICD10Result("123",
                                                                                       [icd10_annotation_result_1])]}

        icd10_annotator_service._ICD10PipelineServiceImpl__pipeline_manager = Mock()
        icd10_annotator_service._ICD10PipelineServiceImpl__db_service = Mock()

        mock_get_item = Mock()
        mock_get_item.return_value = [{"id": "123", "icd10_annotations": []}]
        icd10_annotator_service._ICD10PipelineServiceImpl__db_service.get_item = mock_get_item

        icd10_annotator_service._ICD10PipelineServiceImpl__pipeline_manager.run_pipeline = mock_run_pipeline
        response: ICD10AnnotationResponse = icd10_annotator_service.run_icd10_pipeline(note_id="123", text="text")
        assert response.icd10_annotations[0] == icd10_annotation_result_1
        assert isinstance(icd10_annotator_service._ICD10PipelineServiceImpl__pipeline_components[0],
                          NotePreprocessingComponent)
        assert isinstance(icd10_annotator_service._ICD10PipelineServiceImpl__pipeline_components[1],
                          ACMICD10AnnotationComponent)
        mock_run_pipeline.assert_called_once()
        pipeline_args = mock_run_pipeline.call_args[1]
        assert pipeline_args["id"] == "123"
        assert pipeline_args["text"] == "text"
        pipeline_acm_cache_arg = pipeline_args["acm_cached_result"][0]
        assert pipeline_acm_cache_arg.id == "123"
        assert pipeline_acm_cache_arg.icd10_annotations == []

    @patch("app.service.impl.amazon_icd10_annotator_service.boto3", Mock())
    @patch("app.service.impl.dynamo_db_service.boto3", Mock())
    @patch("app.util.config_manager.ConfigManager.get_specific_config")
    def test__annotate_icd_10__should_return_correct_response__given_correct_input_and_no_cache(self,
                                                                                   mock_get_config: Mock):
        mock_get_config.return_value = "table_name"
        icd10_annotation_1 = ICD10Annotation(code="A15.0", description="Tuberculosis of lung", score=0.7)
        icd10_annotation_2 = ICD10Annotation(code="A15.9", description="Respiratory tuberculosis unspecified",
                                             score=0.54)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=12,
                                                          end_offset=24, is_negated=False,
                                                          suggested_codes=[icd10_annotation_1, icd10_annotation_2],
                                                          raw_acm_response={"data": "data"}
                                                          )

        icd10_annotator_service: ICD10PipelineServiceImpl = ICD10PipelineServiceImpl()

        mock_run_pipeline = Mock()
        mock_run_pipeline.return_value = {DummyComponentOne: [DummyComponentOneResult("a")],
                                          DummyComponentTwo: [DummyComponentTwoResult("b")],
                                          ACMICD10AnnotationComponent: [ACMICD10Result("123",
                                                                                       [icd10_annotation_result_1])]}

        icd10_annotator_service._ICD10PipelineServiceImpl__pipeline_manager = Mock()
        icd10_annotator_service._ICD10PipelineServiceImpl__db_service = Mock()

        mock_get_item = Mock()
        mock_get_item.return_value = []
        icd10_annotator_service._ICD10PipelineServiceImpl__db_service.get_item = mock_get_item

        icd10_annotator_service._ICD10PipelineServiceImpl__pipeline_manager.run_pipeline = mock_run_pipeline
        response: ICD10AnnotationResponse = icd10_annotator_service.run_icd10_pipeline(note_id="123", text="text")
        assert response.icd10_annotations[0] == icd10_annotation_result_1
        assert isinstance(icd10_annotator_service._ICD10PipelineServiceImpl__pipeline_components[0],
                          NotePreprocessingComponent)
        assert isinstance(icd10_annotator_service._ICD10PipelineServiceImpl__pipeline_components[1],
                          ACMICD10AnnotationComponent)
        mock_run_pipeline.assert_called_once()
        pipeline_args = mock_run_pipeline.call_args[1]
        assert pipeline_args["id"] == "123"
        assert pipeline_args["text"] == "text"
        assert pipeline_args["acm_cached_result"] is None


