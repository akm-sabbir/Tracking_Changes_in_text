from unittest import TestCase
from unittest.mock import patch

from app.dto.core.patient_info import PatientInfo
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.pipeline.components.filtericd10_to_hcc_annotation import FilteredICD10ToHccAnnotationComponent
from app.service.pipeline.components.icd10_annotation_filter_component import ICD10AnnotationAlgoComponent


class TestFilteredICD10ToHccAnnotationComponent(TestCase):
    @patch("app.service.impl.amazon_icd10_annotator_service.boto3")
    def test__run__should_return_correct_response__given_correct_input(self, mock_boto3):
        icd10_to_hcc_annotation_component = FilteredICD10ToHccAnnotationComponent()
        params = {"patient_info": PatientInfo(70, "M"), ICD10AnnotationAlgoComponent: self.__get_dummy_icd10_data()}
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

        return [icd10_annotation_result_1, icd10_annotation_result_2]
