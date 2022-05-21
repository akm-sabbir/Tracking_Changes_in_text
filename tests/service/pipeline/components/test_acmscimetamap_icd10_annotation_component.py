from typing import List
from unittest import TestCase
from unittest.mock import Mock, call, patch

from app.dto.core.pipeline.icd10_result import ICD10Result
from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.core.service.Tokens import TokenInfo
from app.dto.core.trie_structure import Trie
from app.dto.core.util.TokenNode import TokenNode
from app.dto.pipeline.changed_word_annotation import ChangedWordAnnotation
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.pipeline.negation_component_result import NegationResult
from app.dto.pipeline.subjective_section import SubjectiveText, SubjectiveSection
from app.dto.pipeline.token_graph_component import GraphTokenResult
from app.dto.pipeline.tokenization_component_result import TokenizationResult
from app.service.impl.amazon_icd10_annotator_service import AmazonICD10AnnotatorServiceImpl
from app.service.impl.icd10_generate_graph_from_text_impl import ICD10GenerateGraphFromTextImpl
from app.service.impl.icd10_positive_sentiment_exclusion_service_impl import ICD10SentimentExclusionServiceImpl
from app.service.impl.pymetamap_icd10_annotator_service import PymetamapICD10AnnotatorService
from app.service.impl.scispacy_icd10_annotator_service import ScispacyICD10AnnotatorService
from app.service.pipeline.components.acmscimetamap_icd10_annotation_component import \
    ACMSciMetamapICD10AnnotationComponent
from app.service.pipeline.components.icd10_token_to_graph_generation_component import TextToGraphGenerationComponent
from app.service.pipeline.components.icd10_tokenizing_text_component import TextTokenizationComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.service.pipeline.components.section_exclusion_service_component import SectionExclusionServiceComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.settings import Settings
from app.util.english_dictionary import EnglishDictionary


class TestICD10AnnotationComponent(TestCase):

    def get_new_node_for_token(self, parent_key: str = "", is_root=True, pos_list: list = [], length: int = 0):
        new_node = TokenNode()
        new_node.pos_tracking = ICD10GenerateGraphFromTextImpl.ROOT_LOCATION
        new_node.pos_list = pos_list
        new_node.is_root = is_root
        new_node.length = length
        new_node.parent_token = parent_key
        return new_node

    word = ["dizziness", "anxiety", "appropriate", "breathlessness", "pain", "groom", "groot", "flurosemide",
            "clonidine", "tuberculosis", "pneumonia"]
    eng_dict = EnglishDictionary()
    root = Trie()
    for each_word in word:
        eng_dict.insert_in(each_word, root)
    Settings.set_settings_dictionary(root)

    @patch("app.service.impl.amazon_icd10_annotator_service.boto3", Mock())
    @patch("app.service.impl.scispacy_icd10_annotator_service.spacy.load", Mock())
    @patch('app.service.impl.scispacy_icd10_annotator_service.termset', Mock())
    @patch("app.service.impl.dynamo_db_service.boto3", Mock())
    @patch("app.util.config_manager.ConfigManager.get_specific_config", Mock())
    @patch("app.service.pipeline.components.acmscimetamap_icd10_annotation_component"
           ".SpanMergerUtil.get_icd_10_codes_with_relevant_spans")
    def test__run__should_return_correct_response__given_correct_input(self, mock_span_util: Mock):
        negation_testing_component = NegationHandlingComponent()
        paragraph1 = Paragraph("He has alot going on, he continues to drinks, daily, no tuberculosis of lung and "
                               "no pneumonia", 0, 68)
        paragraph2 = Paragraph(" he has been feeling dizzy with some fall,he was in the er recently", 91, 157)

        paragraph3 = Paragraph("medication text", 21, 30)
        paragraph4 = Paragraph("flurosemide some other text", 31, 40)

        mock_acm_icd10_service = Mock(AmazonICD10AnnotatorServiceImpl)
        mock_scispacy_icd10_service = Mock(ScispacyICD10AnnotatorService)
        mock_metamap_icd10_service = Mock(PymetamapICD10AnnotatorService)

        mock_icd10_positive_sentiment_exclusion_service = Mock(ICD10SentimentExclusionServiceImpl)
        icd10_annotation_component = ACMSciMetamapICD10AnnotationComponent()

        mock_save_item = Mock()
        mock_save_item.return_value = True
        mock_db_service = Mock()
        mock_db_service.save_item = mock_save_item
        ###############################################################################################################
        test_text_set_one = "He has alot going on, he continues to drinks, daily, nopain, nobreathlessness, " \
                            "and he has been feeling dizzy with some fall,he was in the er recently " \
                            "and he had a head CT, he still smokes, coughing wheezying breathless, withsputum, " \
                            "" \
                            "" \
                            "he stil has urinary incontinent, he has been confirmed to have colon cancer, " \
                            "he am not sure he has hallucinations, he not sleeping well, he has chronic urinary and bowel incontinent, " \
                            "he also chronic"
        test_text_span_set_one_subjective_section = [
            TokenInfo(token="He", start_of_span=0, end_of_span=2, offset=0),
            TokenInfo(token="has", start_of_span=3, end_of_span=6, offset=0),
            TokenInfo(token="alot", start_of_span=7, end_of_span=11, offset=0),
            TokenInfo(token="going", start_of_span=12, end_of_span=17, offset=0),
            TokenInfo(token="on", start_of_span=18, end_of_span=20, offset=0),
            TokenInfo(token=",", start_of_span=20, end_of_span=21, offset=0),
            TokenInfo(token="he", start_of_span=22, end_of_span=24, offset=0),
            TokenInfo(token="has", start_of_span=26, end_of_span=29, offset=0),
            TokenInfo(token="notuberculosis", start_of_span=30, end_of_span=44, offset=0),
            TokenInfo(token="of", start_of_span=45, end_of_span=47, offset=0),
            TokenInfo(token="lung", start_of_span=48, end_of_span=52, offset=0),
            TokenInfo(token="and", start_of_span=53, end_of_span=56, offset=0),
            TokenInfo(token="nopneumonia", start_of_span=57, end_of_span=66, offset=0)]
        test_text_span_set_one_medication_section = [
            TokenInfo(token="continues", start_of_span=25, end_of_span=34, offset=0),
            TokenInfo(token="to", start_of_span=35, end_of_span=37, offset=0),
            TokenInfo(token="drinks", start_of_span=38, end_of_span=44, offset=0),
            TokenInfo(token="daily", start_of_span=46, end_of_span=51, offset=0),
            TokenInfo(token="noclonidine", start_of_span=52, end_of_span=63, offset=0),
            TokenInfo(token="noflurosemide", start_of_span=64, end_of_span=77, offset=0)
        ]
        dict_for_subjective_section = {}
        dict_for_medication_section = {}
        dict_for_subjective_section["nopneumonia"] = {}
        dict_for_subjective_section["nopneumonia"][49] = self.get_new_node_for_token(length=len("nopneumonia"))
        dict_for_subjective_section["notuberculosis"] = {}
        dict_for_subjective_section["notuberculosis"][30] = self.get_new_node_for_token(length=len("notuberculosis"))
        dict_for_subjective_section["lung"] = {}
        dict_for_subjective_section["lung"][48] = self.get_new_node_for_token(length=len("lung"))
        dict_for_subjective_section["of"] = {}
        dict_for_subjective_section["of"][45] = self.get_new_node_for_token(length=len("of"))
        text = paragraph1.text + paragraph2.text
        section_1 = SubjectiveSection(paragraph1.text, 90, 100, 0, 68)
        section_2 = SubjectiveSection(paragraph2.text, 200, 209, 91, 157)

        subjective_text = SubjectiveText(text, [section_1, section_2])
        annotation_results = {SectionExclusionServiceComponent: [],  # need to modify
                              SubjectiveSectionExtractorComponent: [subjective_text],
                              NotePreprocessingComponent: [[paragraph1, paragraph2], [paragraph3, paragraph4]],
                              "acm_cached_result": None, "id": "123", "text": "abcd",
                              TextTokenizationComponent: [TokenizationResult(
                                  complex_container=test_text_span_set_one_subjective_section),
                                  TokenizationResult(
                                      complex_container=test_text_span_set_one_medication_section)],
                              NegationHandlingComponent: [
                                  NegationResult(
                                      paragraph1.text + "\n\n" + paragraph2.text.replace("pneumonia", "Pneumonia")),
                                  NegationResult(
                                      paragraph3.text + "\n\n" + paragraph4.text.replace("flurosemide", "Flurosemide")),
                              ],
                              "changed_words": {"Pneumonia": [ChangedWordAnnotation("pneumonia", "Pneumonia", 11, 20)],
                                                "Flurosemide": [
                                                    ChangedWordAnnotation("flurosemide", "Flurosemide", 31, 40)]},
                              TextToGraphGenerationComponent: [
                                  GraphTokenResult(graph_container=dict_for_subjective_section),
                                  GraphTokenResult(graph_container=dict_for_medication_section)]}

        test_results: List[NegationResult] = negation_testing_component.run(annotation_results)
        ###############################################################################################################

        icd10_annotation_component._ACMSciMetamapICD10AnnotationComponent__acm_icd10_annotation_service = mock_acm_icd10_service
        icd10_annotation_component._ACMSciMetamapICD10AnnotationComponent__scispacy_annotation_service = mock_scispacy_icd10_service
        icd10_annotation_component._ACMSciMetamapICD10AnnotationComponent__metamap_annotation_service = mock_metamap_icd10_service
        icd10_annotation_component._ACMSciMetamapICD10AnnotationComponent__icd10_positive_sentiment_exclusion_service = mock_icd10_positive_sentiment_exclusion_service
        icd10_annotation_component._ACMSciMetamapICD10AnnotationComponent__db_service = mock_db_service

        mock_acm_icd10_service.get_icd_10_codes = Mock()
        mock_acm_icd10_service.get_icd_10_codes.side_effect = self.__get_dummy_icd10_data()
        mock_scispacy_icd10_service.get_icd_10_codes = Mock()
        mock_scispacy_icd10_service.get_icd_10_codes.side_effect = self.__get_dummy_icd10_annotation_result()
        mock_metamap_icd10_service.get_icd_10_codes = Mock()
        mock_metamap_icd10_service.get_icd_10_codes.side_effect = self.__get_dummy_icd10_annotation_result()

        dummy_icd10_result = self.__get_dummy_icd10_annotation_result()
        mock_icd10_positive_sentiment_exclusion_service.get_filtered_annotations_based_on_positive_sentiment = Mock()
        mock_icd10_positive_sentiment_exclusion_service.get_filtered_annotations_based_on_positive_sentiment.return_value = [
            dummy_icd10_result[0][0], dummy_icd10_result[1][0]]

        mock_span_util.side_effect = self.__mock_span_util_side_effect

        acm_result: ICD10Result = icd10_annotation_component.run(annotation_results)[0]
        calls = [call("He has alot going on, he continues to drinks, daily, no tuberculosis of lung and no pneumonia"),
                 call(" he has been feeling dizzy with some fall,he was in the er recently")]

        mock_acm_icd10_service.get_icd_10_codes.assert_has_calls(calls)

        assert mock_acm_icd10_service.get_icd_10_codes.call_count == 2
        icd10_result = acm_result.icd10_annotations

        assert acm_result.id == "123"

        assert acm_result.raw_acm_data[0] == {"raw_data": "data1"}
        assert acm_result.raw_acm_data[1] == {"raw_data": "data2"}

        assert icd10_result[0].begin_offset == 90
        assert icd10_result[0].end_offset == 97
        assert icd10_result[0].medical_condition == "pneumonia"

        assert icd10_result[0].suggested_codes[0].code == "J12.0"
        assert icd10_result[0].suggested_codes[0].description == "Adenoviral pneumonia"
        assert icd10_result[0].suggested_codes[0].score == 0.89

        assert icd10_result[0].suggested_codes[1].code == "J12.89"
        assert icd10_result[0].suggested_codes[1].description == "Other viral pneumonia"
        assert icd10_result[0].suggested_codes[1].score == 0.45
        print(icd10_result[1].medical_condition)
        assert icd10_result[1].begin_offset == 122
        assert icd10_result[1].end_offset == 142
        assert icd10_result[1].medical_condition == "tuberculosis of lung"

        assert icd10_result[1].suggested_codes[0].code == "A15.0"
        assert icd10_result[1].suggested_codes[0].description == "Tuberculosis of lung"
        assert icd10_result[1].suggested_codes[0].score == 0.7

        assert icd10_result[1].suggested_codes[1].code == "A15.9"
        assert icd10_result[1].suggested_codes[1].description == "Respiratory tuberculosis unspecified"
        assert icd10_result[1].suggested_codes[1].score == 0.54

    @patch("app.service.impl.amazon_icd10_annotator_service.boto3", Mock())
    @patch("app.service.impl.scispacy_icd10_annotator_service.spacy.load", Mock())
    @patch('app.service.impl.scispacy_icd10_annotator_service.termset', Mock())
    @patch("app.service.impl.dynamo_db_service.boto3", Mock())
    @patch("app.util.config_manager.ConfigManager.get_specific_config", Mock())
    def test__run__should_return_correct_response__given_correct_input_and_cached_data(self):
        paragraph1 = Paragraph("Tuberculosis some text", 0, 10)
        paragraph2 = Paragraph("Pneumonia some other text", 11, 20)

        paragraph3 = Paragraph("medication text", 21, 30)
        paragraph4 = Paragraph("flurosemide some other text", 31, 40)

        mock_icd10_service = Mock(AmazonICD10AnnotatorServiceImpl)
        icd10_annotation_component = ACMSciMetamapICD10AnnotationComponent()

        mock_save_item = Mock()
        mock_save_item.return_value = True
        mock_db_service = Mock()
        mock_db_service.save_item = mock_save_item

        icd10_annotation_component._ACMICD10AnnotationComponent__icd10_annotation_service = mock_icd10_service
        icd10_annotation_component._ACMICD10AnnotationComponent__db_service = mock_db_service

        mock_icd10_service.get_icd_10_codes = Mock()
        mock_icd10_service.get_icd_10_codes.side_effect = self.__get_dummy_icd10_data()
        dummy_data = self.__get_dummy_icd10_data()
        annotations = [item[1][0] for item in dummy_data]
        raw_acm_data = [item[0][0] for item in dummy_data]
        dummy_result = ICD10Result("123", annotations, raw_acm_data)
        acm_result: ICD10Result = icd10_annotation_component.run(
            {
                NegationHandlingComponent: [
                    paragraph1.text.replace("Tuberculosis", "tuberculosis") + "\n\n" + paragraph2.text,
                    paragraph3.text.replace("flurosemide", "Flurosemide") + "\n\n" + paragraph4.text
                ],
                "text": paragraph1.text + "\n\n" + paragraph2.text,
                NotePreprocessingComponent: [[paragraph1, paragraph2], [paragraph3, paragraph4]],
                "acm_cached_result": [dummy_result], "id": "123"
            })[0]

        mock_icd10_service.get_icd_10_codes.assert_not_called()

        icd10_result = acm_result.icd10_annotations
        assert acm_result.id == "123"

        assert acm_result.raw_acm_data[0] == {"raw_data": "data1"}
        assert acm_result.raw_acm_data[1] == {"raw_data": "data2"}

        assert icd10_result[0].begin_offset == 11
        assert icd10_result[0].end_offset == 15
        assert icd10_result[0].medical_condition == "tuberculosis of lung"

        assert icd10_result[0].suggested_codes[0].code == "A15.0"
        assert icd10_result[0].suggested_codes[0].description == "Tuberculosis of lung"
        assert icd10_result[0].suggested_codes[0].score == 0.7

        assert icd10_result[0].suggested_codes[1].code == "A15.9"
        assert icd10_result[0].suggested_codes[1].description == "Respiratory tuberculosis unspecified"
        assert icd10_result[0].suggested_codes[1].score == 0.54

        assert icd10_result[1].begin_offset == 0
        assert icd10_result[1].end_offset == 7
        assert icd10_result[1].medical_condition == "pneumonia"

        assert icd10_result[1].suggested_codes[0].code == "J12.0"
        assert icd10_result[1].suggested_codes[0].description == "Adenoviral pneumonia"
        assert icd10_result[1].suggested_codes[0].score == 0.89

        assert icd10_result[1].suggested_codes[1].code == "J12.89"
        assert icd10_result[1].suggested_codes[1].description == "Other viral pneumonia"
        assert icd10_result[1].suggested_codes[1].score == 0.45

    def __get_dummy_icd10_annotation_result(self):
        icd10_annotation_1 = ICD10Annotation(code="A15.0", description="Tuberculosis of lung", score=0.7)
        icd10_annotation_2 = ICD10Annotation(code="A15.9", description="Respiratory tuberculosis unspecified",
                                             score=0.54)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="tuberculosis of lung", begin_offset=33,
                                                          end_offset=56, is_negated=False,
                                                          suggested_codes=[icd10_annotation_1, icd10_annotation_2],
                                                          raw_acm_response={"data": "data"})

        icd10_annotation_3 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_4 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)

        icd10_annotation_result_2 = ICD10AnnotationResult(medical_condition="pneumonia", begin_offset=0, end_offset=7,
                                                          is_negated=False,
                                                          suggested_codes=[icd10_annotation_3, icd10_annotation_4],
                                                          raw_acm_response={"data": "data"})

        return [[icd10_annotation_result_1], [icd10_annotation_result_2]]

    def __get_dummy_icd10_data(self):
        icd10_annotation_1 = ICD10Annotation(code="A15.0", description="Tuberculosis of lung", score=0.7)
        icd10_annotation_2 = ICD10Annotation(code="A15.9", description="Respiratory tuberculosis unspecified",
                                             score=0.54)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="tuberculosis of lung", begin_offset=11,
                                                          end_offset=15, is_negated=False,
                                                          suggested_codes=[icd10_annotation_1, icd10_annotation_2],
                                                          raw_acm_response={"data": "data"})

        icd10_annotation_3 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_4 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)

        icd10_annotation_result_2 = ICD10AnnotationResult(medical_condition="pneumonia", begin_offset=0, end_offset=7,
                                                          is_negated=False,
                                                          suggested_codes=[icd10_annotation_3, icd10_annotation_4],
                                                          raw_acm_response={"data": "data"})

        return [([{"raw_data": "data1"}], [icd10_annotation_result_1]),
                ([{"raw_data": "data2"}], [icd10_annotation_result_2])]

    @staticmethod
    def __mock_span_util_side_effect(icd10_annotations, no_of_components_in_algorithm, medant_note):
        return icd10_annotations
