from typing import List
from unittest import TestCase
from unittest.mock import patch, Mock, call

from app.dto.core.pipeline.acm_rxnorm_response import ACMRxNormResult
from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.core.service.Tokens import TokenInfo
from app.dto.core.util.TokenNode import TokenNode
from app.dto.pipeline.changed_word_annotation import ChangedWordAnnotation
from app.dto.pipeline.negation_component_result import NegationResult
from app.dto.pipeline.rxnorm_annotation import RxNormAnnotation
from app.dto.pipeline.rxnorm_annotation_result import RxNormAnnotationResult
from app.dto.pipeline.rxnorm_attribute_annotation import RxNormAttributeAnnotation
from app.dto.pipeline.token_graph_component import GraphTokenResult
from app.service.impl.amazon_rxnorm_annotator_service import AmazonRxNormAnnotatorServiceImpl
from app.service.impl.icd10_generate_graph_from_text_impl import ICD10GenerateGraphFromTextImpl
from app.service.pipeline.components.acm_rxnorm_annotation_component import ACMRxNormAnnotationComponent
from app.service.pipeline.components.icd10_token_to_graph_generation_component import TextToGraphGenerationComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent


class TestACMRxNormAnnotationComponent(TestCase):

    def get_new_node_for_token(self, parent_key: str = "", is_root=True, pos_list: list = [], length: int = 0):
        new_node = TokenNode()
        new_node.pos_tracking = ICD10GenerateGraphFromTextImpl.ROOT_LOCATION
        new_node.pos_list = pos_list
        new_node.is_root = is_root
        new_node.length = length
        new_node.parent_token = parent_key
        return new_node

    @patch("app.service.impl.amazon_icd10_annotator_service.boto3", Mock())
    @patch("app.service.impl.amazon_rxnorm_annotator_service.boto3", Mock())
    @patch("app.service.impl.dynamo_db_service.boto3", Mock())
    @patch("app.util.config_manager.ConfigManager.get_specific_config", Mock())
    @patch("app.util.annotations_alignment_util.AnnotationAlignmentUtil.align_start_and_end_notes_from_annotations")
    def test__run__should_return_correct_response__given_correct_input(self,
                                                                       mock_align_start_and_end_notes_from_annotations
                                                                       ):
        paragraph1 = Paragraph("some text", 0, 10)
        paragraph2 = Paragraph("pneumonia some other text", 11, 20)

        paragraph3 = Paragraph("medication text", 21, 30)
        paragraph4 = Paragraph("flurosemide some other text", 31, 40)

        mock_rxnorm_service = Mock(AmazonRxNormAnnotatorServiceImpl)
        rxnorm_annotation_component = ACMRxNormAnnotationComponent()

        mock_save_item = Mock()
        mock_save_item.return_value = True
        mock_db_service = Mock()
        mock_db_service.save_item = mock_save_item

        mock_rxnorm_service.get_rxnorm_codes = Mock()
        mock_rxnorm_service.get_rxnorm_codes.side_effect = self.__get_dummy_rxnorm_data()

        rxnorm_annotation_component._ACMRxNormAnnotationComponent__rxnorm_annotation_service = mock_rxnorm_service
        rxnorm_annotation_component._ACMRxNormAnnotationComponent__db_service = mock_db_service

        ###############################################################################################################
        test_text_set_one = "He has alot going on, he continues to drinks, daily, nopain, nobreathlessness, " \
                            "and he has been feeling dizzy with some fall,he was in the er recently " \
                            "and he had a head CT, he still smokes, coughing wheezying breathless, withsputum, " \
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
            TokenInfo(token="he", start_of_span=22, end_of_span=24, offset=0)]
        test_text_span_set_one_medication_section = [
            TokenInfo(token="continues", start_of_span=25, end_of_span=34, offset=0),
            TokenInfo(token="to", start_of_span=35, end_of_span=37, offset=0),
            TokenInfo(token="drinks", start_of_span=38, end_of_span=44, offset=0),
            TokenInfo(token="daily", start_of_span=46, end_of_span=51, offset=0),
            TokenInfo(token="nopain", start_of_span=52, end_of_span=58, offset=0),
            TokenInfo(token="nobreathlessness", start_of_span=59, end_of_span=75, offset=0)
        ]
        dict_for_subjective_section = {}
        dict_for_medication_section = {}
        dict_for_subjective_section["has"] = {}
        dict_for_subjective_section["has"][3] = self.get_new_node_for_token(length=len("has"))
        dict_for_medication_section["nopain"] = {}
        dict_for_medication_section["nopain"][46] = self.get_new_node_for_token(length=len("nopain"))
        dict_for_medication_section["nobreathlessness"] = {}
        dict_for_medication_section["nobreathlessness"][54] = self.get_new_node_for_token(
            length=len("nobreathlessness"))
        ###############################################################################################################

        mock_align_start_and_end_notes_from_annotations.return_value = self.__get_aligned_dummy_rxnorm_annotation_result()

        acm_result: ACMRxNormResult = rxnorm_annotation_component.run(
            {NotePreprocessingComponent: [[paragraph1, paragraph2], [paragraph3, paragraph4]],
             "acm_cached_result": None,
             "id": "123",
             NegationHandlingComponent: [
                 NegationResult(paragraph1.text + "\n\n" + paragraph2.text.replace("pneumonia", "Pneumonia")),
                 NegationResult(paragraph3.text + "\n\n" + paragraph4.text.replace("flurosemide", "Flurosemide")),
             ],
             "changed_words": {"Pneumonia": [ChangedWordAnnotation("pneumonia", "Pneumonia", 11, 20)],
                               "Flurosemide": [ChangedWordAnnotation("flurosemide", "Flurosemide", 31, 40)]}
             , TextToGraphGenerationComponent: [GraphTokenResult(dict_for_subjective_section), GraphTokenResult(dict_for_medication_section)]})[0]

        calls = [call("medication text"), call("flurosemide some other text")]

        mock_rxnorm_service.get_rxnorm_codes.assert_has_calls(calls)
        mock_align_start_and_end_notes_from_annotations.assert_called()

        assert mock_rxnorm_service.get_rxnorm_codes.call_count == 2
        rxnorm_result = self.__get_aligned_dummy_rxnorm_annotation_result()

        assert acm_result.id == "123"

        assert acm_result.raw_acm_data[0] == {"raw_data": "data1"}
        assert acm_result.raw_acm_data[1] == {"raw_data": "data2"}

        assert rxnorm_result[0].begin_offset == 101
        assert rxnorm_result[0].end_offset == 110
        assert rxnorm_result[0].medication == "Clonidine"

        assert rxnorm_result[0].suggested_codes[0].code == "2599"
        assert rxnorm_result[0].suggested_codes[0].description == "Clonidine Hydrochloride 0.2 MG Oral Tablet"
        assert rxnorm_result[0].suggested_codes[0].score == 0.7

        assert rxnorm_result[0].suggested_codes[1].code == "884187"
        assert rxnorm_result[0].suggested_codes[
                   1].description == "Clonidine Hydrochloride 0.2 MG Oral Tablet [Catapres]"
        assert rxnorm_result[0].suggested_codes[1].score == 0.54

        assert rxnorm_result[1].begin_offset == 102
        assert rxnorm_result[1].end_offset == 114
        assert rxnorm_result[1].medication == "Flurosemide"

        assert rxnorm_result[1].suggested_codes[0].code == "3456"
        assert rxnorm_result[1].suggested_codes[
                   0].description == "lisdexamfetamine dimesylate 50 MG Oral Capsule [Vyvanse]"
        assert rxnorm_result[1].suggested_codes[0].score == 0.89

        assert rxnorm_result[1].suggested_codes[1].code == "348953"
        assert rxnorm_result[1].suggested_codes[
                   1].description == "lisdexamfetamine dimesylate 50 MG Chewable Tablet [Vyvanse]"
        assert rxnorm_result[1].suggested_codes[1].score == 0.45

    @patch("app.service.impl.amazon_icd10_annotator_service.boto3", Mock())
    @patch("app.service.impl.amazon_rxnorm_annotator_service.boto3", Mock())
    @patch("app.service.impl.dynamo_db_service.boto3", Mock())
    @patch("app.util.config_manager.ConfigManager.get_specific_config", Mock())
    def test__run__should_return_correct_response__given_correct_input_and_cached_data(self):
        paragraph1 = Paragraph("Tuberculosis some text", 0, 10)
        paragraph2 = Paragraph("Pneumonia some other text", 11, 20)

        paragraph3 = Paragraph("medication text", 21, 30)
        paragraph4 = Paragraph("flurosemide some other text", 31, 40)

        mock_rxnorm_service = Mock(AmazonRxNormAnnotatorServiceImpl)
        rxnorm_annotation_component = ACMRxNormAnnotationComponent()

        mock_save_item = Mock()
        mock_save_item.return_value = True
        mock_db_service = Mock()
        mock_db_service.save_item = mock_save_item

        rxnorm_annotation_component._ACMRxNormAnnotationComponent__rxnorm_annotation_service = mock_rxnorm_service
        rxnorm_annotation_component._ACMRxNormAnnotationComponent__db_service = mock_db_service

        mock_rxnorm_service.get_rxnorm_codes = Mock()
        mock_rxnorm_service.get_rxnorm_codes.side_effect = self.__get_dummy_rxnorm_data()
        dummy_data = self.__get_dummy_rxnorm_data()

        annotations = [item[1][0] for item in dummy_data]
        raw_acm_data = [item[0][0] for item in dummy_data]

        dummy_result = ACMRxNormResult("123", annotations, raw_acm_data)
        acm_result: List[ACMRxNormResult] = rxnorm_annotation_component.run(
            {
                NegationHandlingComponent: [
                    paragraph1.text.replace("Tuberculosis", "tuberculosis") + "\n\n" + paragraph2.text,
                    paragraph3.text.replace("flurosemide", "Flurosemide") + "\n\n" + paragraph4.text
                ],
                "text": paragraph1.text + "\n\n" + paragraph2.text,
                NotePreprocessingComponent: [[paragraph1, paragraph2], [paragraph3, paragraph4]],
                "acm_cached_result": [dummy_result], "id": "123"
            })

        mock_rxnorm_service.get_rxnorm_codes.assert_not_called()
        mock_db_service.save_item.assert_not_called()

        assert len(acm_result) == 0

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
                                                            begin_offset=12,
                                                            end_offset=24, is_negated=False,
                                                            suggested_codes=[rxnorm_annotation_1, rxnorm_annotation_2],
                                                            raw_acm_response={"data": "data"})

        rxnorm_annotation_3 = RxNormAnnotation(code="3456",
                                               description="lisdexamfetamine dimesylate 50 MG Oral Capsule [Vyvanse]",
                                               score=0.89)
        rxnorm_annotation_4 = RxNormAnnotation(code="348953",
                                               description="lisdexamfetamine dimesylate 50 MG Chewable Tablet [Vyvanse]",
                                               score=0.45)

        rxnorm_annotation_result_2 = RxNormAnnotationResult(medication="Flurosemide", begin_offset=11,
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
                                                            end_offset=20,
                                                            is_negated=False,
                                                            suggested_codes=[rxnorm_annotation_3, rxnorm_annotation_4],
                                                            raw_acm_response={"data": "data"})

        return [rxnorm_annotation_result_1, rxnorm_annotation_result_2]

    def __get_dummy_rxnorm_data(self):
        return [([{"raw_data": "data1"}], [self.__get_dummy_rxnorm_annotation_result()[0]]),
                ([{"raw_data": "data2"}], [self.__get_dummy_rxnorm_annotation_result()[1]])]

    def __get_aligned_dummy_rxnorm_annotation_result(self):
        rxnorm_annotation_1 = RxNormAnnotation(code="2599", description="Clonidine Hydrochloride 0.2 MG Oral Tablet",
                                               score=0.7)
        rxnorm_annotation_2 = RxNormAnnotation(code="884187",
                                               description="Clonidine Hydrochloride 0.2 MG Oral Tablet [Catapres]",
                                               score=0.54)
        rxnorm_annotation_result_1 = RxNormAnnotationResult(medication="Clonidine", rxnorm_type="GENERIC_NAME",
                                                            attributes=[RxNormAttributeAnnotation(
                                                                attribute_type="STRENGTH",
                                                                score=0.99,
                                                                relationship_score=0.99,
                                                                id=3,
                                                                begin_offset=43,
                                                                end_offset=48,
                                                                text="1.1 %"
                                                            )], begin_offset=101,
                                                            end_offset=110, is_negated=False,
                                                            suggested_codes=[rxnorm_annotation_1, rxnorm_annotation_2],
                                                            raw_acm_response={"data": "data"})

        rxnorm_annotation_3 = RxNormAnnotation(code="3456",
                                               description="lisdexamfetamine dimesylate 50 MG Oral Capsule [Vyvanse]",
                                               score=0.89)
        rxnorm_annotation_4 = RxNormAnnotation(code="348953",
                                               description="lisdexamfetamine dimesylate 50 MG Chewable Tablet [Vyvanse]",
                                               score=0.45)

        rxnorm_annotation_result_2 = RxNormAnnotationResult(medication="Flurosemide", begin_offset=102,
                                                            rxnorm_type="BRAND_NAME",
                                                            attributes=[RxNormAttributeAnnotation(
                                                                attribute_type="ROUTE_OR_MODE",
                                                                score=0.82,
                                                                relationship_score=0.99,
                                                                id=1,
                                                                begin_offset=24,
                                                                end_offset=31,
                                                                text="topical"
                                                            )],
                                                            end_offset=114,
                                                            is_negated=False,
                                                            suggested_codes=[rxnorm_annotation_3, rxnorm_annotation_4],
                                                            raw_acm_response={"data": "data"})

        return [rxnorm_annotation_result_1, rxnorm_annotation_result_2]
