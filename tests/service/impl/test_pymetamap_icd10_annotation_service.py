from typing import List
from unittest import TestCase
from unittest.mock import Mock, patch

from pymetamap import ConceptMMI

from app.dto.core.umls_icd10_data import UMLSICD10Data
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.impl.pymetamap_icd10_annotator_service import PymetamapICD10AnnotatorService


class TestPymetamapICD10AnnotationService(TestCase):

    @patch("app.service.impl.pymetamap_icd10_annotator_service.DependencyInjector.get_instance")
    @patch("app.service.impl.pymetamap_icd10_annotator_service.MetaMap.get_instance")
    def test__get_icd_10_codes__should_return_correct_values__given_correct_input(self, mock_metamap: Mock,
                                                                                  mock_injector: Mock):
        metamap_mock = Mock()
        icd10_mapper_mock = Mock()

        metamap_mock.extract_concepts = Mock()
        concept1 = Mock(ConceptMMI)
        concept1.cui = "123"
        concept1.pos_info = "1/4;2/6"
        concept1.score = 5.13

        concept2 = Mock(ConceptMMI)
        concept2.cui = "127"
        concept2.pos_info = "1/4"
        concept2.score = 5.13

        concept3 = Mock(ConceptMMI)
        concept3.cui = "123"
        concept3.pos_info = "[6/1,8/2], [1/6,3/6]"
        concept3.score = 5.13

        concept4 = Mock(ConceptMMI)
        concept4.cui = "123"
        concept4.pos_info = "1/2,2/3"
        concept4.score = 5.13

        metamap_mock.extract_concepts.return_value = ([concept1, concept2, concept3, concept4], None)

        icd10_mapper_mock.get_umls_data_from_cui = Mock()
        icd10_mapper_mock.get_umls_data_from_cui.return_value = UMLSICD10Data("123", "concept", "definition",
                                                                              "R123.123")

        mock_metamap.return_value = metamap_mock
        mock_injector.return_value = icd10_mapper_mock

        metamap_service = PymetamapICD10AnnotatorService()

        metamap_mock.extract_concepts()
        result: List[ICD10AnnotationResult] = metamap_service.get_icd_10_codes("some text")

        assert result[0].medical_condition == "some"
        assert result[0].begin_offset == 0
        assert result[0].end_offset == 4

        assert result[0].suggested_codes[0].code == "R123.123"
        assert result[0].suggested_codes[0].description == "concept"
        assert result[0].suggested_codes[0].score == 5.13

        assert result[0].suggested_codes[1].code == "R123.123"
        assert result[0].suggested_codes[1].description == "concept"
        assert result[0].suggested_codes[1].score == 5.13

        assert result[1].medical_condition == "text"
        assert result[1].begin_offset == 5
        assert result[1].end_offset == 9
        assert result[1].suggested_codes[0].code == "R123.123"
        assert result[1].suggested_codes[0].description == "concept"
        assert result[1].suggested_codes[0].score == 5.13

        assert result[2].medical_condition == "some"
        assert result[2].begin_offset == 0
        assert result[2].end_offset == 4

        assert result[2].suggested_codes[0].code == "R123.123"
        assert result[2].suggested_codes[0].description == "concept"
        assert result[2].suggested_codes[0].score == 5.13

    @patch("app.service.impl.pymetamap_icd10_annotator_service.DependencyInjector.get_instance")
    @patch("app.service.impl.pymetamap_icd10_annotator_service.MetaMap.get_instance")
    def test__get_icd_10_codes__should_return_empty__given_no_icd110_mappings(self, mock_metamap: Mock,
                                                                              mock_injector: Mock):
        metamap_mock = Mock()
        icd10_mapper_mock = Mock()

        metamap_mock.extract_concepts = Mock()
        concept = Mock(ConceptMMI)
        concept.cui = "123"
        concept.pos_info = "1/4"
        concept.score = 5.13
        metamap_mock.extract_concepts.return_value = ([concept], None)

        icd10_mapper_mock.get_umls_data_from_cui = Mock()
        icd10_mapper_mock.get_umls_data_from_cui.return_value = UMLSICD10Data("123", "concept", "definition",
                                                                              "")

        mock_metamap.return_value = metamap_mock
        mock_injector.return_value = icd10_mapper_mock

        metamap_service = PymetamapICD10AnnotatorService()

        metamap_mock.extract_concepts()
        result: List[ICD10AnnotationResult] = metamap_service.get_icd_10_codes("some text")

        assert len(result) == 0
