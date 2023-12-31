from unittest import TestCase
from unittest.mock import patch, Mock

from app.dto.core.patient_info import PatientInfo
from app.dto.core.pipeline.icd10_result import ICD10Result
from app.dto.core.service.hcc_code import HCCCode
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.service.pipeline.components.acmscimetamap_icd10_annotation_component import \
    ACMSciMetamapICD10AnnotationComponent
from app.service.pipeline.components.filtericd10_to_hcc_annotation import FilteredICD10ToHccAnnotationComponent


class TestFilteredICD10ToHccAnnotationComponent(TestCase):
    @patch("app.service.impl.amazon_icd10_annotator_service.boto3")
    @patch("app.service.pipeline.components.filtericd10_to_hcc_annotation.HCCServiceImpl")
    def test__run__should_return_correct_response__given_correct_input(self, mock_hcc_service: Mock, mock_boto3: Mock):
        hcc_service_mock = Mock()
        mock_hcc_service.return_value = hcc_service_mock
        hcc_service_mock.get_hcc_risk_scores = Mock()
        mock_hcc_response = Mock(HCCResponseDto)
        mock_hcc_response.hcc_maps = {
            "J449": HCCCode(code="HCC111", score=0.335),
            "E109": HCCCode(code="HCC19", score=0.106),
        }
        hcc_service_mock.get_hcc_risk_scores.return_value = mock_hcc_response
        icd10_to_hcc_annotation_component = FilteredICD10ToHccAnnotationComponent()
        params = {"patient_info": PatientInfo(70, "M"),
                  ACMSciMetamapICD10AnnotationComponent: self.__get_dummy_icd10_data()}
        results = icd10_to_hcc_annotation_component.run(params)

        assert len(results[0].hcc_maps) == 2
        assert results[0].hcc_maps["J449"].code == "HCC111"
        assert results[0].hcc_maps["J449"].score == 0.335

        assert results[0].hcc_maps["E109"].code == "HCC19"
        assert results[0].hcc_maps["E109"].score == 0.106

    def __get_dummy_icd10_data(self):
        icd10_annotation_1 = ICD10Annotation(code="G47.00", description="Tuberculosis of lung", score=0.7)
        icd10_annotation_2 = ICD10Annotation(code="M25.40", description="Respiratory tuberculosis unspecified",
                                             score=0.54)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=12,
                                                          end_offset=24, is_negated=False,
                                                          suggested_codes=[icd10_annotation_1, icd10_annotation_2])

        icd10_annotation_3 = ICD10Annotation(code="E10.9", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_4 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)
        icd10_annotation_5 = ICD10Annotation(code="J44.9", description="Other viral pneumonia",
                                             score=0.72)

        icd10_annotation_result_2 = ICD10AnnotationResult(medical_condition="pneumonia", begin_offset=45, end_offset=54,
                                                          is_negated=True,
                                                          suggested_codes=[icd10_annotation_3, icd10_annotation_4,
                                                                           icd10_annotation_5])
        mock_result = Mock(ICD10Result)
        mock_result.icd10_annotations = [icd10_annotation_result_1, icd10_annotation_result_2]
        return [mock_result]
