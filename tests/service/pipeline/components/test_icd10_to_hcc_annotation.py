from unittest import TestCase
from unittest.mock import Mock, patch

from app.dto.core.pipeline.icd10_result import ICD10Result
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.pipeline.icd10_hcc_meta_info import Icd10HccMeta
from app.service.impl.icd10_annotation_service_with_filters_impl import ICD10AnnotatorServiceWithFilterImpl
from app.service.pipeline.components.acmscimetamap_icd10_annotation_component import \
    ACMSciMetamapICD10AnnotationComponent
from app.service.pipeline.components.icd10_annotation_filter_component import ICD10AnnotationAlgoComponent
from app.service.pipeline.components.icd10_to_hcc_annotation import ICD10ToHccAnnotationComponent
from app.settings import Settings


class TestICD10ToHccAnnotationComponent(TestCase):
    Settings.exclusion_dict = {}

    @patch("app.service.impl.amazon_icd10_annotator_service.boto3")
    @patch("app.service.pipeline.components.icd10_to_hcc_annotation.HCCServiceImpl")
    def test__run__should_return_correct_response__given_correct_input(self, mock_hcc_service, mock_boto3):
        icd10_annotation_filter_component = ICD10AnnotationAlgoComponent()
        icd10_to_hcc_annotation_component = ICD10ToHccAnnotationComponent()
        icd10_annotation_filter_component._ICD10AnnotationAlgoComponent__icd10_annotation_service_with_filters = \
            Mock(ICD10AnnotatorServiceWithFilterImpl)

        params = {"dx_threshold": 0.9, "icd10_threshold": 0.67, "parent_threshold": 0.80,
                  ACMSciMetamapICD10AnnotationComponent: [ICD10Result("123", self.__get_dummy_icd10_data(), [{}])]
                  }
        results: list[Icd10HccMeta] = icd10_to_hcc_annotation_component.run(params)

        assert len(results[0].hcc_annotation_response.hcc_maps) == 0

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
