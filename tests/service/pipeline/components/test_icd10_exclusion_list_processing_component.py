from unittest import TestCase
from unittest.mock import Mock, patch

from app.dto.core.pipeline.acm_icd10_response import ACMICD10Result
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.pipeline.icd10_hcc_meta_info import Icd10HccMeta
from app.service.impl.icd10_annotation_service_with_filters_impl import ICD10AnnotatorServiceWithFilterImpl
from app.service.pipeline.components.icd10_annotation_filter_component import ICD10AnnotationAlgoComponent
from app.service.pipeline.components.icd10_exclusion_list_processing_component import CodeExclusionHandlingComponent
from app.service.pipeline.components.icd10_to_hcc_annotation import ICD10ToHccAnnotationComponent
from app.service.impl.icd10_exclusion_list_processing_service_impl import Icd10CodeExclusionServiceImpl
from app.service.pipeline.components.acm_icd10_annotation_component import ACMICD10AnnotationComponent
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.dto.core.service.hcc_code import HCCCode
from app import app_base_path
from app.util.config_manager import ConfigManager
import os
from app.settings import Settings
from app.dto.pipeline.icd10_meta_info import ICD10MetaInfo


class MockedIcd10ExclusionServiceImpl():
    def __init__(self,):
        pass

    def get_icd_10_code_exclusion_decision(self, icd10_metainfo: dict):
        icd101 = Mock(ICD10MetaInfo)
        icd101.hcc_map = "HCC85"
        icd101.score = 0.80
        icd101.length = 5
        icd101.entity_score = 0.99
        icd101.remove = True
        icd102 = Mock(ICD10MetaInfo)
        icd102.hcc_map = "HCC85"
        icd102.score = 0.67
        icd102.length = 6
        icd102.entity_score = 0.99
        icd102.remove = True
        icd103 = Mock(ICD10MetaInfo)
        icd103.hcc_map = "HCC85"
        icd103.score = 0.71
        icd103.length = 4
        icd103.entity_score = 0.91
        icd103.remove = False
        icd104 = Mock(ICD10MetaInfo)
        icd104.hcc_map = "HCC85"
        icd104.score = 0.82
        icd104.length = 3
        icd104.entity_score = 0.99
        icd104.remove = False
        icd105 = Mock(ICD10MetaInfo)
        icd105.hcc_map = "HCC85"
        icd105.score = 0.87
        icd105.length = 5
        icd105.entity_score = 0.99
        icd105.remove = False
        param = {"A0531": icd101, "A40421": icd102, "A853": icd103, "A04": icd104, "A7421": icd105}
        return param


class TestExclusionHandlingComponent(TestCase):

    icd10_exclusion_dict: dict = {"A04": ["A05-", "A1832"], "A05": ["A404-", "A32-", "T61-T62", "A040-A044", "A02-"],
                                  "A06": ["A07-"], "A08": ["J09X3", "J102", "J112"], "A09": ["K529", "R197"],
                                  "A30": ["B92"],
                                  "A32": ["P372"], "A35": ["A34", "A33"], "A40": ["P360-P361", "O85", "A4181"],
                                  "A41": ["A40-", "O85", "R7881", "P36-"], "A42": ["B471"], "A46": ["O8689"],
                                  "A48": ["B471"],
                                  "A49": ["A699", "A749", "B95-B96", "A799", "A399"], "A56": ["P391", "P231"],
                                  "A71": ["B940"],
                                  "A74": ["M023-", "A55-A56", "P391", "P231"], "A75": ["A7981"],
                                  "A85": ["B262", "A872", "B258", "B004", "G933", "B020", "B100-", "B050", "A80-"]}

    @patch("app.service.impl.amazon_icd10_annotator_service.boto3")
    @patch.object(CodeExclusionHandlingComponent, "_CodeExclusionHandlingComponent__icd10_exclusion_handling_service",
                  MockedIcd10ExclusionServiceImpl())
    def test__run__should_return_correct_response__given_correct_input(self, mock_boto3):
        icd10_exclusion_list_processing: CodeExclusionHandlingComponent = CodeExclusionHandlingComponent()
        icd10_annotation_filter_component = ICD10AnnotationAlgoComponent()
        icd10_to_hcc_annotation_component = ICD10ToHccAnnotationComponent()
        icd10_annotation_filter_component._ICD10AnnotationAlgoComponent__icd10_annotation_service_with_filters = \
            Mock(ICD10AnnotatorServiceWithFilterImpl)
        icd101 = Mock(ICD10MetaInfo)
        icd101.hcc_map = "HCC85"
        icd101.score = 0.80
        icd101.length = 5
        icd101.entity_score = 0.99
        icd101.remove = False
        icd102 = Mock(ICD10MetaInfo)
        icd102.hcc_map = "HCC85"
        icd102.score = 0.67
        icd102.length = 6
        icd102.entity_score = 0.99
        icd102.remove = False
        icd103 = Mock(ICD10MetaInfo)
        icd103.hcc_map = "HCC85"
        icd103.score = 0.71
        icd103.length = 4
        icd103.entity_score = 0.91
        icd103.remove = False
        icd104 = Mock(ICD10MetaInfo)
        icd104.hcc_map = "HCC85"
        icd104.score = 0.82
        icd104.length = 3
        icd104.entity_score = 0.99
        icd104.remove = False
        icd105 = Mock(ICD10MetaInfo)
        icd105.hcc_map = "HCC85"
        icd105.score = 0.87
        icd105.length = 5
        icd105.entity_score = 0.99
        icd105.remove = False
        icd10_hcc_meta_info = {"A0531": icd101, "A40421": icd102, "A853": icd103, "A04": icd104, "A7421": icd105}
        mock_hcc_response = Mock(HCCResponseDto)
        mock_hcc_code = Mock(HCCCode)
        mock_hcc_code.code = "HCC100"
        mock_hcc_code.score = 0.7
        mock_hcc_response.hcc_maps = {"I5030": mock_hcc_code}
        mock_icd10_hcc_meta_info = Mock(Icd10HccMeta)
        mock_icd10_hcc_meta_info.hcc_annotation_response = mock_hcc_response
        mock_icd10_hcc_meta_info.hcc_meta_map_info = icd10_hcc_meta_info
        params = {"dx_threshold": 0.9, "icd10_threshold": 0.67, "parent_threshold": 0.80,
                  ACMICD10AnnotationComponent: [ACMICD10Result("123", self.__get_dummy_icd10_data(), [{}])],
                  ICD10ToHccAnnotationComponent: [mock_icd10_hcc_meta_info]
                  }
        results = icd10_exclusion_list_processing.run(params)
        assert len(results[0].icd10_annotations[1].suggested_codes) == 3

    def __get_dummy_icd10_data(self):
        icd10_annotation_1 = ICD10Annotation(code="A05.31", description="Tuberculosis of lung", score=0.8)
        icd10_annotation_2 = ICD10Annotation(code="A40.421", description="Respiratory tuberculosis unspecified",
                                             score=0.67)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=12,
                                                          end_offset=24, is_negated=False,
                                                          suggested_codes=[icd10_annotation_1, icd10_annotation_2])

        icd10_annotation_3 = ICD10Annotation(code="A85.3", description="Adenoviral pneumonia", score=0.71)
        icd10_annotation_4 = ICD10Annotation(code="A04", description="Other viral pneumonia",
                                             score=0.82)
        icd10_annotation_5 = ICD10Annotation(code="A7421", description="Other viral pneumonia",
                                             score=0.87)

        icd10_annotation_result_2 = ICD10AnnotationResult(medical_condition="pneumonia", begin_offset=45, end_offset=54,
                                                          is_negated=True,
                                                          suggested_codes=[icd10_annotation_3, icd10_annotation_4,
                                                                           icd10_annotation_5])

        return [icd10_annotation_result_1, icd10_annotation_result_2]
