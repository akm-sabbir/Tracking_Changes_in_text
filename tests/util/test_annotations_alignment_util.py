from typing import List
from unittest import TestCase
from unittest.mock import Mock, patch

from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.core.service.Tokens import TokenInfo
from app.dto.core.trie_structure import Trie
from app.dto.core.util.TokenNode import TokenNode
from app.dto.pipeline.changed_word_annotation import ChangedWordAnnotation
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.pipeline.medication_section import MedicationText, MedicationSection
from app.dto.pipeline.negation_component_result import NegationResult
from app.dto.pipeline.rxnorm_annotation import RxNormAnnotation
from app.dto.pipeline.rxnorm_annotation_result import RxNormAnnotationResult
from app.dto.pipeline.rxnorm_attribute_annotation import RxNormAttributeAnnotation
from app.dto.pipeline.subjective_section import SubjectiveSection, SubjectiveText
from app.dto.pipeline.token_graph_component import GraphTokenResult
from app.dto.pipeline.tokenization_component_result import TokenizationResult
from app.service.impl.icd10_generate_graph_from_text_impl import ICD10GenerateGraphFromTextImpl
from app.service.pipeline.components.icd10_token_to_graph_generation_component import TextToGraphGenerationComponent
from app.service.pipeline.components.icd10_tokenizing_text_component import TextTokenizationComponent
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent
from app.settings import Settings
from app.util.annotations_alignment_util import AnnotationAlignmentUtil
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.util.english_dictionary import EnglishDictionary


class TestAnnotationsAlignmentUtil(TestCase):

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

    @patch('app.util.config_manager.ConfigManager.get_specific_config')
    def test__align_start_and_end_notes_from_annotations__given_correct_ontology__should_align_notes(self, mock_get_config: Mock):
        negation_testing_component = NegationHandlingComponent()
        mock_get_config.return_value = "10"
        paragraph1 = Paragraph("He has alot going on, he continues to drinks, daily, no tuberculosis and no pneumonia", 0, 62)
        paragraph2 = Paragraph(" he has been feeling dizzy with some fall,he was in the er recently", 91, 157)

        paragraph3 = Paragraph("continues to  drinks daily no clonidine no flurosemide", 25, 79)
        paragraph4 = Paragraph(" he am not sure he has hallucinations, he not sleeping well, he has chronic urinary and bowel incontinent", 131, 40)

        text = paragraph1.text + paragraph2.text
        section_1 = SubjectiveSection(paragraph1.text, 90, 100, 0, 60)
        section_2 = SubjectiveSection(paragraph2.text, 200, 209, 91, 157)

        subjective_text = SubjectiveText(text, [section_1, section_2])

        text = paragraph3.text + paragraph4.text
        section_3 = MedicationSection(paragraph3.text, 90, 100, 25, 77)
        section_4 = MedicationSection(paragraph4.text, 200, 209, 131, 40)

        medication_text = MedicationText(text, [section_3, section_4])
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
            TokenInfo(token="and", start_of_span=45, end_of_span=48, offset=0),
            TokenInfo(token="nopneumonia", start_of_span=49, end_of_span=60, offset=0)]
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
        dict_for_medication_section["noclonidine"] = {}
        dict_for_medication_section["noclonidine"][52] = self.get_new_node_for_token(length=len("noclonidine"))
        dict_for_medication_section["noflurosemide"] = {}
        dict_for_medication_section["noflurosemide"][64] = self.get_new_node_for_token(
            length=len("noflurosemide"))
        annotation_results = {"text": test_text_set_one,
                                                       "acm_cached_result": None, "changed_words": {},
                                                       TextTokenizationComponent: [TokenizationResult(
                                                           complex_container=test_text_span_set_one_subjective_section),
                                                                                   TokenizationResult(
                                                                                       complex_container=test_text_span_set_one_medication_section)],
                                                       TextToGraphGenerationComponent: [GraphTokenResult(
                                                           graph_container=dict_for_subjective_section),
                                                                                        GraphTokenResult(
                                                                                            graph_container=dict_for_medication_section)],
                                                       SubjectiveSectionExtractorComponent: [
                                                           SubjectiveText(test_text_set_one, [])],
                                                       MedicationSectionExtractorComponent: [
                                                           MedicationText(test_text_set_one, [])]
                                                       }
        test_results: List[NegationResult] = negation_testing_component.run(annotation_results)
        assert test_results[1].tokens_with_span[5].token == 'clonidine'
        assert test_results[1].tokens_with_span[5].start_of_span == 55
        assert test_results[1].tokens_with_span[5].end_of_span == 64
        assert test_results[1].tokens_with_span[5].offset == 0
        assert test_results[1].tokens_with_span[7].token == "flurosemide"
        assert test_results[1].tokens_with_span[7].start_of_span == 68
        assert test_results[1].tokens_with_span[7].end_of_span == 79
        assert test_results[0].tokens_with_span[9].token == 'tuberculosis'
        assert test_results[0].tokens_with_span[9].start_of_span == 33
        assert test_results[0].tokens_with_span[9].end_of_span == 45
        assert test_results[0].tokens_with_span[9].offset == 0
        assert test_results[0].tokens_with_span[12].token == "pneumonia"
        assert test_results[0].tokens_with_span[12].start_of_span == 53
        assert test_results[0].tokens_with_span[12].end_of_span == 62
        ###############################################################################################################


        mock_annotation_results = {
            MedicationSectionExtractorComponent: [medication_text],
            SubjectiveSectionExtractorComponent: [subjective_text],
            NegationHandlingComponent: [
                NegationResult(paragraph1.text + "\n\n" + paragraph2.text.replace("pneumonia", "Pneumonia")),
                NegationResult(paragraph3.text + "\n\n" + paragraph4.text.replace("flurosemide", "Flurosemide")),
            ],
            "changed_words": {"Pneumonia": [ChangedWordAnnotation("pneumonia", "Pneumonia", 11, 20)],
                              "Flurosemide": [ChangedWordAnnotation("flurosemide", "Flurosemide", 31, 40)]}
        }

        mock_acm_result = Mock()
        mock_acm_result.rxnorm_annotations = self.__get_dummy_rxnorm_annotation_result()
        mock_acm_result.icd10_annotations = self.__get_dummy_icd10_annotation_result()

        AnnotationAlignmentUtil.align_start_and_end_notes_from_annotations("ICD10-CM", mock_acm_result,
                                                                           mock_annotation_results,
                                                                           annotation_results[TextToGraphGenerationComponent][0].graph_token_container)
        print(annotation_results[TextToGraphGenerationComponent][1].graph_token_container)
        AnnotationAlignmentUtil.align_start_and_end_notes_from_annotations("RxNorm", mock_acm_result,
                                                                           mock_annotation_results,
                                                                           annotation_results[TextToGraphGenerationComponent][1].graph_token_container)

        assert mock_acm_result.rxnorm_annotations[0].begin_offset == 119
        assert mock_acm_result.rxnorm_annotations[0].end_offset == 128
        assert mock_acm_result.rxnorm_annotations[1].begin_offset == 131
        assert mock_acm_result.rxnorm_annotations[1].end_offset == 142

        assert mock_acm_result.icd10_annotations[0].begin_offset == 122
        assert mock_acm_result.icd10_annotations[0].end_offset == 134
        assert mock_acm_result.icd10_annotations[1].begin_offset == 141
        assert mock_acm_result.icd10_annotations[1].end_offset == 150

    def test__set_annotation_condition__given_correct_ontology__should_assign_condition(self):
        rxnorm_annotation = Mock(RxNormAnnotationResult)
        rxnorm_annotation.medication = "clonidine"

        icd10_annotation = Mock(ICD10AnnotationResult)
        icd10_annotation.medical_condition = "pneumonia"

        mock_rxnorm_matched_value = "Clonidine"
        mock_icd10_matched_value = "Pneumonia"

        AnnotationAlignmentUtil._AnnotationAlignmentUtil__set_annotation_condition("RxNorm", rxnorm_annotation,
                                                                                   mock_rxnorm_matched_value)
        AnnotationAlignmentUtil._AnnotationAlignmentUtil__set_annotation_condition("ICD10-CM", icd10_annotation,
                                                                                   mock_icd10_matched_value)

        assert rxnorm_annotation.medication == mock_rxnorm_matched_value
        assert icd10_annotation.medical_condition == mock_icd10_matched_value

    def test__get_annotation_text__given_incorrect_ontology__should_raise_exception(self):
        with self.assertRaises(ValueError) as error:
            AnnotationAlignmentUtil._AnnotationAlignmentUtil__get_annotation_text("some text", [])
        assert error.exception.args[0] == "Unknown note to align!"

    def __get_dummy_icd10_annotation_result(self):
        icd10_annotation_1 = ICD10Annotation(code="A15.0", description="Tuberculosis of lung", score=0.7)
        icd10_annotation_2 = ICD10Annotation(code="A15.9", description="Respiratory tuberculosis unspecified",
                                             score=0.54)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=33,
                                                          end_offset=45, is_negated=False,
                                                          suggested_codes=[icd10_annotation_1, icd10_annotation_2],
                                                          raw_acm_response={"data": "data"})

        icd10_annotation_3 = ICD10Annotation(code="J12.0", description="Adenoviral pneumonia", score=0.89)
        icd10_annotation_4 = ICD10Annotation(code="J12.89", description="Other viral pneumonia",
                                             score=0.45)

        icd10_annotation_result_2 = ICD10AnnotationResult(medical_condition="Pneumonia", begin_offset=53, end_offset=62,
                                                          is_negated=False,
                                                          suggested_codes=[icd10_annotation_3, icd10_annotation_4],
                                                          raw_acm_response={"data": "data"})

        return [icd10_annotation_result_1, icd10_annotation_result_2]

    def __get_dummy_rxnorm_annotation_result(self):
        rxnorm_annotation_1 = RxNormAnnotation(code="2599", description="Clonidine Hydrochloride 0.2 MG Oral Tablet",
                                               score=0.7)
        rxnorm_annotation_2 = RxNormAnnotation(code="884187",
                                               description="Clonidine Hydrochloride 0.2 MG Oral Tablet [Catapres]",
                                               score=0.54)
        rxnorm_annotation_result_1 = RxNormAnnotationResult(medication="Clonidine", rxnorm_type="GENERIC_NAME",
                                                            attributes=[RxNormAttributeAnnotation(
                                                                score=0.82,
                                                                attribute_type="ROUTE_OR_MODE",
                                                                relationship_score=0.99,
                                                                id=1,
                                                                begin_offset=24,
                                                                end_offset=31,
                                                                text="topical"
                                                            )],
                                                            begin_offset=55,
                                                            end_offset=64, is_negated=False,
                                                            suggested_codes=[rxnorm_annotation_1, rxnorm_annotation_2],
                                                            raw_acm_response={"data": "data"})

        rxnorm_annotation_3 = RxNormAnnotation(code="3456",
                                               description="lisdexamfetamine dimesylate 50 MG Oral Capsule [Vyvanse]",
                                               score=0.89)
        rxnorm_annotation_4 = RxNormAnnotation(code="348953",
                                               description="lisdexamfetamine dimesylate 50 MG Chewable Tablet [Vyvanse]",
                                               score=0.45)

        rxnorm_annotation_result_2 = RxNormAnnotationResult(medication="Flurosemide", begin_offset=68,
                                                            rxnorm_type="BRAND_NAME",
                                                            attributes=[RxNormAttributeAnnotation(
                                                                attribute_type="ROUTE_OR_MODE",
                                                                score=0.82,
                                                                relationship_score=0.99,
                                                                id=3,
                                                                begin_offset=24,
                                                                end_offset=31,
                                                                text="topical"
                                                            )],
                                                            end_offset=79,
                                                            is_negated=False,
                                                            suggested_codes=[rxnorm_annotation_3, rxnorm_annotation_4],
                                                            raw_acm_response={"data": "data"})

        return [rxnorm_annotation_result_1, rxnorm_annotation_result_2]
