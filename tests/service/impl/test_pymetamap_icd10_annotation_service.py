from typing import List
from unittest import TestCase
from unittest.mock import Mock, patch

from app.dto.core.umls_icd10_data import UMLSICD10Data
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.impl.pymetamap_icd10_annotator_service import PymetamapICD10AnnotatorService


class TestPymetamapICD10AnnotationService(TestCase):

    @patch("app.service.impl.pymetamap_icd10_annotator_service.DependencyInjector.get_instance")
    @patch("app.util.config_manager.ConfigManager.get_specific_config")
    @patch("app.util.rest_client_util.RestClientUtil.post_sync")
    def test__get_icd_10_codes__should_return_correct_values__given_correct_input(self, mock_post: Mock,
                                                                                  mock_config_manager: Mock,
                                                                                  mock_injector: Mock):
        mock_config_manager.return_value = "some url"
        icd10_mapper_mock = Mock()

        concept1 = {"cui": "123", "mm": "MMI", "posInfo": "1/4;2/6", "score": "5.13",
                    "trigger": '["Isopod"-ab-1-"isopod"-adj-1]'}
        concept2 = {"cui": "127", "mm": "MMI", "posInfo": "1/4", "score": "5.13",
                    "trigger": '["Isopod"-ab-1-"isopod"-adj-1]'}
        concept3 = {"cui": "123", "mm": "MMI", "posInfo": "[6/1,8/2], [1/6,3/6]", "score": "5.13",
                    "trigger": '["Isopod"-ab-1-"isopod"-adj-0]'}
        concept4 = {"cui": "123", "posInfo": "1/2,2/3", "score": "5.13", "trigger": '["Isopod"-ab-1-"isopod"-adj-1]'}

        mock_response = Mock()
        mock_response.json = Mock()
        mock_response.json.return_value = [concept1, concept2, concept3, concept4]

        mock_post.return_value = mock_response

        icd10_mapper_mock.get_umls_data_from_cui = Mock()
        icd10_mapper_mock.get_umls_data_from_cui.return_value = UMLSICD10Data("123", "concept", "definition",
                                                                              "R123.123")

        mock_injector.return_value = icd10_mapper_mock

        metamap_service = PymetamapICD10AnnotatorService()

        result: List[ICD10AnnotationResult] = metamap_service.get_icd_10_codes("some text")

        assert len(result) == 2
        assert result[0].medical_condition == "some"
        assert result[0].begin_offset == 0
        assert result[0].end_offset == 4
        assert result[0].is_negated is True

        assert result[0].suggested_codes[0].code == "R123.123"
        assert result[0].suggested_codes[0].description == "concept"
        assert result[0].suggested_codes[0].score == 5.13

        assert result[0].suggested_codes[1].code == "R123.123"
        assert result[0].suggested_codes[1].description == "concept"
        assert result[0].suggested_codes[1].score == 5.13

        assert result[1].medical_condition == "text"
        assert result[1].begin_offset == 5
        assert result[1].end_offset == 9
        assert result[0].is_negated is True

        assert result[1].suggested_codes[0].code == "R123.123"
        assert result[1].suggested_codes[0].description == "concept"
        assert result[1].suggested_codes[0].score == 5.13

    @patch("app.service.impl.pymetamap_icd10_annotator_service.DependencyInjector.get_instance")
    @patch("app.util.config_manager.ConfigManager.get_specific_config")
    @patch("app.util.rest_client_util.RestClientUtil.post_sync")
    def test__get_icd_10_codes__should_return_empty__given_no_icd10_mappings(self, mock_post: Mock,
                                                                             mock_config_manager: Mock,
                                                                             mock_injector: Mock):
        mock_config_manager.return_value = "some url"
        icd10_mapper_mock = Mock()

        concept1 = {"cui": "123", "mm": "MMI", "posInfo": "1/4;2/6", "score": "5.13"}
        concept2 = {"cui": "127", "mm": "MMI", "posInfo": "1/4", "score": "5.13"}
        concept3 = {"cui": "123", "mm": "MMI", "posInfo": "[6/1,8/2], [1/6,3/6]", "score": "5.13"}
        concept4 = {"cui": "123", "mm": "MMI", "posInfo": "1/2,2/3", "score": "5.13"}

        mock_response = Mock()
        mock_response.json = Mock()
        mock_response.json.return_value = [concept1, concept2, concept3, concept4]

        mock_post.return_value = mock_response

        icd10_mapper_mock.get_umls_data_from_cui = Mock()
        icd10_mapper_mock.get_umls_data_from_cui.return_value = UMLSICD10Data("123", "concept", "definition", "")

        mock_injector.return_value = icd10_mapper_mock

        metamap_service = PymetamapICD10AnnotatorService()
        result: List[ICD10AnnotationResult] = metamap_service.get_icd_10_codes("some text")

        assert len(result) == 0
