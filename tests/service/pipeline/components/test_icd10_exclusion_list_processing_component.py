from unittest import TestCase
from unittest.mock import Mock, patch

from app.dto.core.pipeline.acm_icd10_response import ACMICD10Result
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.impl.icd10_annotation_service_with_filters_impl import ICD10AnnotatorServiceWithFilterImpl
from app.service.pipeline.components.icd10_annotation_filter_component import ICD10AnnotationAlgoComponent
from app.service.pipeline.components.icd10_to_hcc_annotation import ICD10ToHccAnnotationComponent
from app.service.pipeline.components.icd10_exclusion_list_processing_component import ExclusionHandlingComponent
from app.service.pipeline.components.acm_icd10_annotation_component import ACMICD10AnnotationComponent
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.dto.core.service.hcc_code import HCCCode
from app import app_base_path
from app.util.config_manager import ConfigManager
import os
from app.Settings import Settings
from app.dto.pipeline.icd10_meta_info import icd10_meta_info


class TestICD10ExclusionService(TestCase):
    @patch("app.service.impl.amazon_icd10_annotator_service.boto3")
    def test__run__should_return_correct_response__given_correct_input(self, mock_boto3):
        exclusion_list_folder = ConfigManager.get_specific_config(section="exclusion", key="list_")
        exclusion_list_ = os.path.join(os.path.join(os.path.dirname(app_base_path),
                                                    exclusion_list_folder), "exclusions.json")
        Settings.set_exclusion_dict(exclusion_list_)
        icd10_annotation_filter_component = ICD10AnnotationAlgoComponent()
        icd10_to_hcc_annotation_component = ICD10ToHccAnnotationComponent()
        icd10_exclusion_list_processing = ExclusionHandlingComponent()
        icd10_annotation_filter_component._ICD10AnnotationAlgoComponent__icd10_annotation_service_with_filters = \
            Mock(ICD10AnnotatorServiceWithFilterImpl)
        mock_hcc_response = Mock(HCCResponseDto)
        mock_hcc_code = Mock(HCCCode)
        mock_hcc_code.code = "HCC100"
        mock_hcc_code.score = 0.7
        mock_meta_icd10info1 = Mock(icd10_meta_info)
        mock_meta_icd10info2 = Mock(icd10_meta_info)
        mock_meta_icd10info3 = Mock(icd10_meta_info)
        mock_meta_icd10info4 = Mock(icd10_meta_info)
        mock_meta_icd10info1.hcc_map = "HCC85"
        mock_meta_icd10info1.score = 0.7
        mock_meta_icd10info1.entity_score: float = 0.91
        mock_meta_icd10info1.length: int = 5
        mock_meta_icd10info1.remove: bool = False

        mock_meta_icd10info2.hcc_map = "HCC85"
        mock_meta_icd10info2.score = 0.8
        mock_meta_icd10info2.entity_score: float = 0.91
        mock_meta_icd10info2.length: int = 4
        mock_meta_icd10info2.remove: bool = False

        mock_meta_icd10info3.hcc_map = "HCC18"
        mock_meta_icd10info3.score = 0.84
        mock_meta_icd10info3.entity_score: float = 0.98
        mock_meta_icd10info3.length: int = 5
        mock_meta_icd10info3.remove: bool = False

        mock_meta_icd10info4.hcc_map = "HCC88"
        mock_meta_icd10info4.score = 0.67
        mock_meta_icd10info4.entity_score: float = 0.99
        mock_meta_icd10info4.length: int = 4
        mock_meta_icd10info4.remove: bool = False
        icd10_hcc_meta_info = {"I5030": mock_meta_icd10info1, "I509": mock_meta_icd10info2, "E1169":
            mock_meta_icd10info3, "I209": mock_meta_icd10info4 }
        mock_hcc_response.hcc_maps = {"I5030": mock_hcc_code}
        params = {"dx_threshold": 0.9, "icd10_threshold": 0.67, "parent_threshold": 0.80,
                  ACMICD10AnnotationComponent: [ACMICD10Result("123", self.__get_dummy_icd10_data(), [{}])],
                  ICD10ToHccAnnotationComponent: [mock_hcc_response, icd10_hcc_meta_info]
                  }
        results = icd10_exclusion_list_processing.run(params)

        assert len(results[0].hcc_maps) == 0

    def __get_dummy_icd10_data(self):
        icd10_annotation_1 = ICD10Annotation(code="G47.00", description="Tuberculosis of lung", score=0.7)
        icd10_annotation_2 = ICD10Annotation(code="M25.40", description="Respiratory tuberculosis unspecified",
                                             score=0.54)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=12,
                                                          end_offset=24, is_negated=False,
                                                          suggested_codes=[icd10_annotation_1, icd10_annotation_2])

        icd10_annotation_3 = ICD10Annotation(code="T38.805S", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_4 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)
        icd10_annotation_5 = ICD10Annotation(code="J12", description="Other viral pneumonia",
                                             score=0.72)

        icd10_annotation_result_2 = ICD10AnnotationResult(medical_condition="pneumonia", begin_offset=45, end_offset=54,
                                                          is_negated=True,
                                                          suggested_codes=[icd10_annotation_3, icd10_annotation_4,
                                                                           icd10_annotation_5])

        return [icd10_annotation_result_1, icd10_annotation_result_2]
