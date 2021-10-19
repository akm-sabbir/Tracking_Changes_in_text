from unittest import TestCase
from unittest.mock import Mock, patch

from app.dto.pipeline.dummy_component_four_result import DummyComponentFourResult
from app.dto.pipeline.dummy_component_one_result import DummyComponentOneResult
from app.dto.pipeline.dummy_component_three_result import DummyComponentThreeResult
from app.dto.pipeline.dummy_component_two_result import DummyComponentTwoResult
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.response.icd10_annotation_response import ICD10AnnotationResponse
from app.service.impl.icd10_pipeline_service_algorithm_impl import ICD10PipelineServiceAlgoImpl
from app.service.pipeline.components import icd10_to_hcc_annotation
from app.service.pipeline.components.icd10_annotation_component import ICD10AnnotationComponent
from app.service.pipeline.components.icd10_annotation_filter_component import ICD10AnnotationAlgoComponent
from app.service.pipeline.components.icd10_to_hcc_annotation import ICD10ToHccAnnotationComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from tests.service.pipeline.components.dummy_component_four import DummyComponentThree, DummyComponentFour
from tests.service.pipeline.components.dummy_component_one import DummyComponentOne
from tests.service.pipeline.components.dummy_component_two import DummyComponentTwo


class TestICD10PipelineServiceAlgoImpl(TestCase):

    @patch("app.service.impl.amazon_icd10_annotator_service.boto3")
    def test__annotate_icd_10_algo__should_return_correct_response__given_correct_input(self, mock_boto3):
        icd10_annotation_1 = ICD10Annotation(code="A15.0", description="Tuberculosis of lung", score=0.8)
        icd10_annotation_2 = ICD10Annotation(code="A15.9", description="Respiratory tuberculosis unspecified",
                                             score=0.68)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=12,
                                                          end_offset=24, is_negated=False,
                                                          suggested_codes=[icd10_annotation_1, icd10_annotation_2])

        icd10_annotator_service_algo: ICD10PipelineServiceAlgoImpl = ICD10PipelineServiceAlgoImpl()

        mock_run_pipeline = Mock()
        mock_run_pipeline.return_value = {DummyComponentOne: [DummyComponentOneResult("a")],
                                          DummyComponentTwo: [DummyComponentTwoResult("b")],
                                          DummyComponentThree: [DummyComponentThreeResult("c")],
                                          DummyComponentFour: [DummyComponentFourResult("d")],
                                          ICD10AnnotationAlgoComponent: [icd10_annotation_result_1]}

        icd10_annotator_service_algo._ICD10PipelineServiceAlgoImpl__pipeline_manager = Mock()
        icd10_annotator_service_algo._ICD10PipelineServiceAlgoImpl__pipeline_manager.run_pipeline = mock_run_pipeline
        response: ICD10AnnotationResponse = icd10_annotator_service_algo.run_icd10_pipeline(text="text",
                                                                                            dx_threshold=0.9,
                                                                                            icd10_threshold=0.7,
                                                                                            parent_threshold=0.81)
        assert response.icd10_annotations[0] == icd10_annotation_result_1
        assert isinstance(icd10_annotator_service_algo._ICD10PipelineServiceAlgoImpl__pipeline_components[0],
                          NotePreprocessingComponent)
        assert isinstance(icd10_annotator_service_algo._ICD10PipelineServiceAlgoImpl__pipeline_components[1],
                          ICD10AnnotationComponent)
        assert isinstance(icd10_annotator_service_algo._ICD10PipelineServiceAlgoImpl__pipeline_components[2],
                          ICD10ToHccAnnotationComponent)
        assert isinstance(icd10_annotator_service_algo._ICD10PipelineServiceAlgoImpl__pipeline_components[3],
                          ICD10AnnotationAlgoComponent)
        mock_run_pipeline.assert_called_once_with(text='text', dx_threshold=0.9,
                                                                icd10_threshold=0.7,
                                                                parent_threshold=0.81)
