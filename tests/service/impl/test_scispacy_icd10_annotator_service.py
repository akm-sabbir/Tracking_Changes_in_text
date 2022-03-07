from unittest import TestCase
from unittest.mock import Mock, patch

import spacy

from app.dto.core.umls_icd10_data import UMLSICD10Data
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.icd10_annotator_service import ICD10AnnotatorService
from app.service.impl.scispacy_icd10_annotator_service import ScispacyICD10AnnotatorService


class TestScispacyICD10AnnotatorService(TestCase):
    @patch('app.service.impl.scispacy_icd10_annotator_service.spacy.load', Mock())
    @patch('app.service.impl.scispacy_icd10_annotator_service.DependencyInjector.get_instance',
           Mock())
    @patch(
        'app.service.impl.scispacy_icd10_annotator_service.ScispacyICD10AnnotatorService._map_to_annotation_result_dto')
    def test__get_icd_10_codes__should_return_correct_response__given_correct_input(self, annotation_mock: Mock):
        scispacy_annotator: ICD10AnnotatorService = ScispacyICD10AnnotatorService("en_ner_bc5cdr_md", "umls2021")

        annotation_mock.return_value = self.__get_dummy_icd10_data()
        mock_icd10_codes = scispacy_annotator.get_icd_10_codes("Diabetes, heart attack.")

        annotation_mock.assert_called_once()
        assert mock_icd10_codes == self.__get_dummy_icd10_data()

    @patch('app.service.impl.scispacy_icd10_annotator_service.spacy.load', Mock())
    @patch('app.service.impl.scispacy_icd10_annotator_service.DependencyInjector.get_instance',
           Mock())
    @patch('app.service.impl.scispacy_icd10_annotator_service.ScispacyICD10AnnotatorService._map_cui_to_icd10_code')
    def test__map_to_annotation_result_dto__should_return_correct_response__given_correct_input(self,
                                                                                                mock_map_cui_to_icd10: Mock):
        mock_map_cui_to_icd10.return_value = self.__get_dummy_icd10_annotation_list()
        mock_entities = self.__get_dummy_entities()
        scispacy_annotator: ICD10AnnotatorService = ScispacyICD10AnnotatorService("some model", "some umls knowledge")

        annotator_icd10_results = scispacy_annotator._map_to_annotation_result_dto(mock_entities)

        assert annotator_icd10_results[0].medical_condition == "some entity 1"
        assert annotator_icd10_results[0].score == None
        assert annotator_icd10_results[0].begin_offset == 0
        assert annotator_icd10_results[0].end_offset == 12
        assert annotator_icd10_results[0].is_negated == False
        assert annotator_icd10_results[0].suggested_codes == self.__get_dummy_icd10_annotation_list()

        assert annotator_icd10_results[1].medical_condition == "some entity 2"
        assert annotator_icd10_results[1].score == None
        assert annotator_icd10_results[1].begin_offset == 14
        assert annotator_icd10_results[1].end_offset == 25
        assert annotator_icd10_results[1].is_negated == False
        assert annotator_icd10_results[1].suggested_codes == self.__get_dummy_icd10_annotation_list()

    @patch('app.service.impl.scispacy_icd10_annotator_service.spacy.load', Mock())
    @patch('app.service.impl.scispacy_icd10_annotator_service.DependencyInjector.get_instance')
    def test__map_cui_to_icd10_code__should_return_correct_response__given_correct_input(self, mock_icd10_mapper: Mock):
        icd10_mapper_mock = Mock()
        icd10_mapper_mock.get_icd10_from_cui = Mock()
        icd10_mapper_mock.get_umls_data_from_cui = Mock()

        icd10_mapper_mock.get_umls_data_from_cui.return_value = UMLSICD10Data("123", "concept", "definition",
                                                                              "R123.123")
        icd10_mapper_mock.get_icd10_from_cui.return_value = "R123.123"
        mock_icd10_mapper.return_value = icd10_mapper_mock

        dummy_umls_entities = self.__get_dummy_umls_ents()
        scispacy_annotator: ICD10AnnotatorService = ScispacyICD10AnnotatorService("en_ner_bc5cdr_md", "umls2021")

        annotator_icd10_codes = scispacy_annotator._map_cui_to_icd10_code(dummy_umls_entities)

        assert annotator_icd10_codes[0].code == "R123.123"
        assert annotator_icd10_codes[0].description == "concept"
        assert annotator_icd10_codes[0].score == 0.67

        assert annotator_icd10_codes[1].code == "R123.123"
        assert annotator_icd10_codes[1].description == "concept"
        assert annotator_icd10_codes[1].score == 0.97

    def __get_dummy_umls_ents(self):
        return [('CUI124012', 0.67), ('CUI125012', 0.97)]

    def __get_dummy_icd10_annotation_list(self):
        dummy_icd10_data = self.__get_dummy_icd10_data()[0]
        return dummy_icd10_data.suggested_codes

    def __get_dummy_entities(self):
        dummy_entity1 = Mock(spacy.tokens.span.Span)
        dummy_entity1.text = "some entity 1"
        dummy_entity1.start_char = 0
        dummy_entity1.end_char = 12

        dummy_entity2 = Mock(spacy.tokens.span.Span)
        dummy_entity2.text = "some entity 2"
        dummy_entity2.start_char = 14
        dummy_entity2.end_char = 25

        return [dummy_entity1, dummy_entity2]

    def __get_dummy_icd10_data(self):
        icd10_annotation_1 = ICD10Annotation(code="A15.0", description="Tuberculosis of lung", score=0.7)
        icd10_annotation_2 = ICD10Annotation(code="A15.9", description="Respiratory tuberculosis unspecified",
                                             score=0.54)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="Affect is normal", begin_offset=12,
                                                          end_offset=24, is_negated=False,
                                                          suggested_codes=[icd10_annotation_1, icd10_annotation_2],
                                                          raw_acm_response={"data": "data"})

        icd10_annotation_3 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_4 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)

        icd10_annotation_result_2 = ICD10AnnotationResult(medical_condition="sleeping well", begin_offset=45,
                                                          end_offset=54,
                                                          is_negated=True,
                                                          suggested_codes=[icd10_annotation_3, icd10_annotation_4],
                                                          raw_acm_response={"data": "data"})

        icd10_annotation_5 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_6 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)

        icd10_annotation_result_3 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=40,
                                                          end_offset=50,
                                                          is_negated=False,
                                                          suggested_codes=[icd10_annotation_5, icd10_annotation_6],
                                                          raw_acm_response={"data": "data"})

        return [icd10_annotation_result_1, icd10_annotation_result_2, icd10_annotation_result_3]
