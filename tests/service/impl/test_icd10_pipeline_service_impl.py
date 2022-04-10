import asyncio
from asyncio import AbstractEventLoop
from unittest import TestCase
from unittest.mock import Mock, patch

from app.dto.core.icd10_pipeline_params import ICD10PipelineParams
from app.dto.core.patient_info import PatientInfo
from app.dto.core.pipeline.icd10_result import ICD10Result
from app.dto.core.service.hcc_code import HCCCode
from app.dto.pipeline.dummy_component_one_result import DummyComponentOneResult
from app.dto.pipeline.dummy_component_two_result import DummyComponentTwoResult
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.dto.response.icd10_annotation_response import ICD10AnnotationResponse
from app.service.impl.icd10_pipeline_service_impl import ICD10PipelineServiceImpl
from app.service.pipeline.components.acmscimetamap_icd10_annotation_component import \
    ACMSciMetamapICD10AnnotationComponent
from app.service.pipeline.components.acm_rxnorm_annotation_component import ACMRxNormAnnotationComponent
from app.service.pipeline.components.filtericd10_to_hcc_annotation import FilteredICD10ToHccAnnotationComponent
from app.service.pipeline.components.icd10_annotation_filter_component import ICD10AnnotationAlgoComponent
from app.service.pipeline.components.icd10_exclusion_list_processing_component import CodeExclusionHandlingComponent
from app.service.pipeline.components.icd10_to_hcc_annotation import ICD10ToHccAnnotationComponent
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.service.pipeline.components.section_exclusion_service_component import SectionExclusionServiceComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.service.pipeline.components.icd10_smoking_pattern_detection import PatientSmokingConditionDetectionComponent
from tests.service.pipeline.components.dummy_component_one import DummyComponentOne
from tests.service.pipeline.components.dummy_component_two import DummyComponentTwo
from app.settings import Settings
from app.dto.pipeline.smoker_condition import PatientSmokingCondition


class TestICD10PipelineServiceImpl(TestCase):
    __loop: AbstractEventLoop

    @classmethod
    def setUpClass(cls):
        cls.__loop = asyncio.new_event_loop()

    @classmethod
    def tearDownClass(cls):
        cls.__loop.close()

    @patch("app.service.impl.amazon_icd10_annotator_service.boto3", Mock())
    @patch("app.service.impl.amazon_rxnorm_annotator_service.boto3", Mock())
    @patch("app.service.impl.scispacy_icd10_annotator_service.spacy.load", Mock())
    @patch('app.service.impl.scispacy_icd10_annotator_service.termset', Mock())
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
        Settings.nlp_smoker_detector = Mock()
        icd10_annotator_service: ICD10PipelineServiceImpl = ICD10PipelineServiceImpl()

        mock_run_pipeline = Mock()

        hcc_maps = {"A123": HCCCode(code="HCC108", score=0.5)}
        mock_hcc_maps = HCCResponseDto(hcc_maps=hcc_maps,
                                       demographics_score={},
                                       disease_interactions_score={},
                                       aggregated_risk_score=0.0,
                                       demographics_details={})

        mock_acm_response = Mock(ICD10Result)
        mock_acm_response.raw_acm_data = [{"acm_data": "data"}]
        mock_acm_response.icd10_annotations = self.__get_dummy_icd10_data()
        mock_smoking_detection_response = PatientSmokingCondition()
        mock_run_pipeline.return_value = {DummyComponentOne: [DummyComponentOneResult("a")],
                                          DummyComponentTwo: [DummyComponentTwoResult("b")],
                                          FilteredICD10ToHccAnnotationComponent: [mock_hcc_maps],
                                          ACMSciMetamapICD10AnnotationComponent: [mock_acm_response],
                                          PatientSmokingConditionDetectionComponent: [mock_smoking_detection_response]
                                          }

        icd10_annotator_service._ICD10PipelineServiceImpl__pipeline_manager = Mock()
        icd10_annotator_service._ICD10PipelineServiceImpl__db_service = Mock()

        mock_get_item = Mock()
        mock_get_item.return_value = [{"id": "123", "icd10_annotations": []}]
        icd10_annotator_service._ICD10PipelineServiceImpl__db_service.get_item = mock_get_item

        icd10_annotator_service._ICD10PipelineServiceImpl__pipeline_manager.run_pipeline = mock_run_pipeline
        pipeline_params = ICD10PipelineParams("123", "text", 0.7, 0.7, 0.7, True, PatientInfo(70, "M"))

        response: ICD10AnnotationResponse = self.__loop.run_until_complete(
            icd10_annotator_service.run_icd10_pipeline(pipeline_params))
        assert response.icd10_annotations[0] == icd10_annotation_result_1
        assert response.id == "123"
        assert response.hcc_maps == mock_hcc_maps
        assert response.raw_acm_data == mock_acm_response.raw_acm_data

        component_serial = [PatientSmokingConditionDetectionComponent,
                                      SectionExclusionServiceComponent,
                                      SubjectiveSectionExtractorComponent, MedicationSectionExtractorComponent,
                                      NegationHandlingComponent, NotePreprocessingComponent,
                                      ACMSciMetamapICD10AnnotationComponent, ACMRxNormAnnotationComponent,
                                      ICD10ToHccAnnotationComponent,
                                      CodeExclusionHandlingComponent,
                                      ICD10AnnotationAlgoComponent,
                                      FilteredICD10ToHccAnnotationComponent]

        for idx, type in enumerate(component_serial):
            assert isinstance(icd10_annotator_service._ICD10PipelineServiceImpl__pipeline_components[idx], type)

        mock_run_pipeline.assert_called_once()
        pipeline_args = mock_run_pipeline.call_args[1]
        assert pipeline_args["id"] == "123"
        assert pipeline_args["text"] == "text"
        assert pipeline_args["dx_threshold"] == 0.7
        assert pipeline_args["icd10_threshold"] == 0.7
        assert pipeline_args["parent_threshold"] == 0.7

        pipeline_acm_cache_arg = pipeline_args["acm_cached_result"][0]
        assert pipeline_acm_cache_arg.id == "123"
        assert pipeline_acm_cache_arg.icd10_annotations == []

    @patch("app.service.impl.amazon_icd10_annotator_service.boto3", Mock())
    @patch("app.service.impl.amazon_rxnorm_annotator_service.boto3", Mock())
    @patch("app.service.impl.scispacy_icd10_annotator_service.spacy.load", Mock())
    @patch('app.service.impl.scispacy_icd10_annotator_service.termset', Mock())
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

        hcc_maps = {"A123": HCCCode(code="HCC108", score=0.5)}
        mock_hcc_maps = HCCResponseDto(hcc_maps=hcc_maps,
                                       demographics_score={},
                                       disease_interactions_score={},
                                       aggregated_risk_score=0.0,
                                       demographics_details={})

        mock_acm_response = Mock(ICD10Result)
        mock_acm_response.raw_acm_data = [{"acm_data": "data"}]
        mock_acm_response.icd10_annotations = self.__get_dummy_icd10_data()
        mock_smoking_detection_response = PatientSmokingCondition()

        mock_run_pipeline = Mock()
        mock_run_pipeline.return_value = {DummyComponentOne: [DummyComponentOneResult("a")],
                                          DummyComponentTwo: [DummyComponentTwoResult("b")],
                                          FilteredICD10ToHccAnnotationComponent: [mock_hcc_maps],
                                          ACMSciMetamapICD10AnnotationComponent: [mock_acm_response],
                                          PatientSmokingConditionDetectionComponent: [mock_smoking_detection_response]
                                          }

        icd10_annotator_service._ICD10PipelineServiceImpl__pipeline_manager = Mock()
        icd10_annotator_service._ICD10PipelineServiceImpl__db_service = Mock()

        mock_get_item = Mock()
        mock_get_item.return_value = []
        icd10_annotator_service._ICD10PipelineServiceImpl__db_service.get_item = mock_get_item

        icd10_annotator_service._ICD10PipelineServiceImpl__pipeline_manager.run_pipeline = mock_run_pipeline
        pipeline_params = ICD10PipelineParams("123", "text", 0.7, 0.7, 0.7, False, PatientInfo(70, "M"))

        response: ICD10AnnotationResponse = self.__loop.run_until_complete(
            icd10_annotator_service.run_icd10_pipeline(pipeline_params))
        assert response.icd10_annotations[0] == icd10_annotation_result_1

        component_serial = [PatientSmokingConditionDetectionComponent,
                                      SectionExclusionServiceComponent,
                                      SubjectiveSectionExtractorComponent, MedicationSectionExtractorComponent,
                                      NegationHandlingComponent, NotePreprocessingComponent,
                                      ACMSciMetamapICD10AnnotationComponent, ACMRxNormAnnotationComponent,
                                      ICD10ToHccAnnotationComponent,
                                      CodeExclusionHandlingComponent,
                                      ICD10AnnotationAlgoComponent,
                                      FilteredICD10ToHccAnnotationComponent]

        for idx, type in enumerate(component_serial):
            assert isinstance(icd10_annotator_service._ICD10PipelineServiceImpl__pipeline_components[idx], type)

            mock_run_pipeline.assert_called_once()
        pipeline_args = mock_run_pipeline.call_args[1]
        assert pipeline_args["id"] == "123"
        assert pipeline_args["text"] == "text"
        assert pipeline_args["dx_threshold"] == 0.7
        assert pipeline_args["icd10_threshold"] == 0.7
        assert pipeline_args["parent_threshold"] == 0.7
        assert pipeline_args["acm_cached_result"] is None

    def __get_dummy_icd10_data(self):
        icd10_annotation_1 = ICD10Annotation(code="A15.0", description="Tuberculosis of lung", score=0.7)
        icd10_annotation_2 = ICD10Annotation(code="A15.9", description="Respiratory tuberculosis unspecified",
                                             score=0.54)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=12,
                                                          end_offset=24, is_negated=False,
                                                          suggested_codes=[icd10_annotation_1, icd10_annotation_2])

        icd10_annotation_3 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_4 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)
        icd10_annotation_5 = ICD10Annotation(code="J12", description="Other viral pneumonia",
                                             score=0.72)

        icd10_annotation_result_2 = ICD10AnnotationResult(medical_condition="pneumonia", begin_offset=45, end_offset=54,
                                                          is_negated=True,
                                                          suggested_codes=[icd10_annotation_3, icd10_annotation_4,
                                                                           icd10_annotation_5])

        return [icd10_annotation_result_1, icd10_annotation_result_2]
