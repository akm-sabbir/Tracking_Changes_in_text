from typing import List
from unittest import TestCase

from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.exception.service_exception import ServiceException
from app.service.pipeline.components.dummy_component_one import DummyComponentOne
from app.service.pipeline.components.dummy_component_two import DummyComponentTwo
from app.service.pipeline.components.icd10_annotation_dummy_component import ICD10AnnotationDummyComponent
from app.service.pipeline.pipeline_manager import PipelineManager


class TestPipelineManager(TestCase):

    def test__run_pipeline__should_return_correct_response__given_correct_components(self):
        pipeline_components = [DummyComponentOne(), DummyComponentTwo(), ICD10AnnotationDummyComponent()]
        pipeline_result = PipelineManager(pipeline_components).run_pipeline(text='text')
        assert pipeline_result[DummyComponentOne][0].message == "text"
        assert pipeline_result[DummyComponentTwo][0].message == "dummy two"
        dummy_icd10_results: List[ICD10AnnotationResult] = pipeline_result[ICD10AnnotationDummyComponent]
        assert dummy_icd10_results[0].begin_offset == 12
        assert dummy_icd10_results[0].end_offset == 24
        assert dummy_icd10_results[0].medical_condition == "Tuberculosis"

        assert dummy_icd10_results[0].suggested_codes[0].code == "A15.0"
        assert dummy_icd10_results[0].suggested_codes[0].description == "Tuberculosis of lung"
        assert dummy_icd10_results[0].suggested_codes[0].score == 0.7

        assert dummy_icd10_results[0].suggested_codes[1].code == "A15.9"
        assert dummy_icd10_results[0].suggested_codes[1].description == "Respiratory tuberculosis unspecified"
        assert dummy_icd10_results[0].suggested_codes[1].score == 0.54

        assert dummy_icd10_results[1].begin_offset == 45
        assert dummy_icd10_results[1].end_offset == 54
        assert dummy_icd10_results[1].medical_condition == "pneumonia"

        assert dummy_icd10_results[1].suggested_codes[0].code == "J12.0"
        assert dummy_icd10_results[1].suggested_codes[0].description == "Adenoviral pneumonia"
        assert dummy_icd10_results[1].suggested_codes[0].score == 0.89

        assert dummy_icd10_results[1].suggested_codes[1].code == "J12.89"
        assert dummy_icd10_results[1].suggested_codes[1].description == "Other viral pneumonia"
        assert dummy_icd10_results[1].suggested_codes[1].score == 0.45

    def test__run_pipeline__should_raise_exception__given_dependencies_not_added(self):
        with self.assertRaises(ServiceException) as error:
            pipeline_components = [DummyComponentTwo(), ICD10AnnotationDummyComponent()]
            PipelineManager(pipeline_components).run_pipeline({})
        assert str(error.exception) == "Dependencies of " + DummyComponentTwo.__name__ + " not satisfied"
