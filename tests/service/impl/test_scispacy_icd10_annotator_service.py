from unittest import TestCase
from unittest.mock import Mock, patch

import spacy
from spacy.lang.en import English
from spacy.tokens import Doc

from app.dto.core.umls_icd10_data import UMLSICD10Data
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.service.icd10_annotator_service import ICD10AnnotatorService
from app.service.impl.scispacy_icd10_annotator_service import ScispacyICD10AnnotatorService


class TestScispacyICD10AnnotatorService(TestCase):
    @patch('app.service.impl.scispacy_icd10_annotator_service.ConfigManager.get_specific_config', Mock())
    @patch('app.service.impl.scispacy_icd10_annotator_service.termset', Mock())
    @patch('app.service.impl.scispacy_icd10_annotator_service.spacy.load')
    @patch('app.service.impl.scispacy_icd10_annotator_service.DependencyInjector.get_instance')
    def test__get_icd_10_codes__should_return_correct_response__given_correct_input(self,
                                                                                    mock_icd10_mapper: Mock,
                                                                                    mock_nlp: Mock):
        icd10_mapper_mock = Mock()
        icd10_mapper_mock.get_icd10_from_cui = Mock()
        icd10_mapper_mock.get_umls_data_from_cui = Mock()
        icd10_mapper_mock.get_umls_data_from_cui.return_value = UMLSICD10Data("123", "concept", "definition",
                                                                              "R123.123")

        icd10_mapper_mock.get_icd10_from_cui.return_value = "R123.123"

        mock_icd10_mapper.return_value = icd10_mapper_mock
        mock_nlp.return_value = self.__get_dummy_spacy_object()

        scispacy_annotator: ICD10AnnotatorService = ScispacyICD10AnnotatorService()

        mock_icd10_codes = scispacy_annotator.get_icd_10_codes("Diabetes, heart attack.")

        mock_nlp.assert_called_once()

        assert mock_icd10_codes[0].medical_condition == "some entity 1"
        assert mock_icd10_codes[0].begin_offset == 0
        assert mock_icd10_codes[0].end_offset == 12
        assert mock_icd10_codes[0].suggested_codes == [ICD10Annotation(code='R123.123', description='concept', score=0.67),
                                                       ICD10Annotation(code='R123.123', description='concept', score=0.97)]

        assert mock_icd10_codes[1].medical_condition == "some entity 2"
        assert mock_icd10_codes[1].begin_offset == 14
        assert mock_icd10_codes[1].end_offset == 25
        assert mock_icd10_codes[1].suggested_codes == [
            ICD10Annotation(code='R123.123', description='concept', score=0.67),
            ICD10Annotation(code='R123.123', description='concept', score=0.97)]

    @patch('app.service.impl.scispacy_icd10_annotator_service.ConfigManager.get_specific_config', Mock())
    @patch('app.service.impl.scispacy_icd10_annotator_service.termset', Mock())
    @patch('app.service.impl.scispacy_icd10_annotator_service.spacy.load')
    @patch('app.service.impl.scispacy_icd10_annotator_service.DependencyInjector.get_instance')
    def test__get_icd_10_codes__should_return_empty_response__given_incorrect_input(self,
                                                                                    mock_icd10_mapper: Mock,
                                                                                    mock_nlp: Mock):
        icd10_mapper_mock = Mock()
        icd10_mapper_mock.get_icd10_from_cui = Mock()
        icd10_mapper_mock.get_umls_data_from_cui = Mock()
        icd10_mapper_mock.get_umls_data_from_cui.return_value = UMLSICD10Data("", None, None,
                                                                              "")

        icd10_mapper_mock.get_icd10_from_cui.return_value = ""

        mock_icd10_mapper.return_value = icd10_mapper_mock
        mock_nlp.return_value = self.__get_dummy_spacy_object()

        scispacy_annotator: ICD10AnnotatorService = ScispacyICD10AnnotatorService()

        mock_icd10_codes = scispacy_annotator.get_icd_10_codes("Diabetes, heart attack.")

        mock_nlp.assert_called_once()

        assert mock_icd10_codes[0].medical_condition == "some entity 1"
        assert mock_icd10_codes[0].begin_offset == 0
        assert mock_icd10_codes[0].end_offset == 12
        assert mock_icd10_codes[0].suggested_codes == []

        assert mock_icd10_codes[1].medical_condition == "some entity 2"
        assert mock_icd10_codes[1].begin_offset == 14
        assert mock_icd10_codes[1].end_offset == 25
        assert mock_icd10_codes[1].suggested_codes == []

    def __get_dummy_spacy_object(self):
        mock_entities = Mock(Doc)
        mock_entities.ents = self.__get_dummy_entities()

        mock_nlp = Mock(English)
        mock_nlp.return_value = mock_entities

        return mock_nlp

    def __get_dummy_entities(self):
        dummy_entity1 = Mock(spacy.tokens.span.Span)
        dummy_entity1.text = "some entity 1"
        dummy_entity1.start_char = 0
        dummy_entity1.end_char = 12
        dummy_entity1._.kb_ents = [('CUI124012', 0.67), ('CUI125012', 0.97)]
        dummy_entity1._.negex = True

        dummy_entity2 = Mock(spacy.tokens.span.Span)
        dummy_entity2.text = "some entity 2"
        dummy_entity2.start_char = 14
        dummy_entity2.end_char = 25
        dummy_entity2._.kb_ents = [('CUI124012', 0.67), ('CUI125012', 0.97)]
        dummy_entity2._.negex = False

        return (dummy_entity1, dummy_entity2)
