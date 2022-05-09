from unittest import TestCase
from unittest.mock import Mock, call, patch

from app.dto.core.pipeline.icd10_result import ICD10Result
from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.pipeline.changed_word_annotation import ChangedWordAnnotation
from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.dto.pipeline.negation_component_result import NegationResult
from app.dto.pipeline.subjective_section import SubjectiveText, SubjectiveSection
from app.service.impl.amazon_icd10_annotator_service import AmazonICD10AnnotatorServiceImpl
from app.service.impl.icd10_positive_sentiment_exclusion_service_impl import ICD10SentimentExclusionServiceImpl
from app.service.impl.pymetamap_icd10_annotator_service import PymetamapICD10AnnotatorService
from app.service.impl.scispacy_icd10_annotator_service import ScispacyICD10AnnotatorService
from app.service.pipeline.components.acmscimetamap_icd10_annotation_component import \
    ACMSciMetamapICD10AnnotationComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.service.pipeline.components.section_exclusion_service_component import SectionExclusionServiceComponent
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent


class TestICD10AnnotationComponent(TestCase):
    @patch("app.service.impl.amazon_icd10_annotator_service.boto3", Mock())
    @patch("app.service.impl.scispacy_icd10_annotator_service.spacy.load", Mock())
    @patch('app.service.impl.scispacy_icd10_annotator_service.termset', Mock())
    @patch("app.service.impl.dynamo_db_service.boto3", Mock())
    @patch("app.util.config_manager.ConfigManager.get_specific_config", Mock())
    @patch("app.service.pipeline.components.acmscimetamap_icd10_annotation_component.TextPreprocessorUtil.get_preprocessed_text")
    @patch(
        "app.service.pipeline.components.acmscimetamap_icd10_annotation_component.SpanMergerUtil.get_icd_10_codes_with_relevant_spans")
    def test__run__should_return_correct_response__given_correct_input(self, mock_span_util: Mock,
                                                                       mock_text_preprocessor: Mock):
        paragraph1 = Paragraph("Some TEXT", 0, 10)
        paragraph2 = Paragraph("pneumonia some other text", 11, 20)

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
        mock_text_preprocessor.side_effect = self.__mock_text_preprocessor_util_side_effect

        text = paragraph1.text + paragraph2.text
        section_1 = SubjectiveSection(paragraph1.text, 90, 100, 0, 30)
        section_2 = SubjectiveSection(paragraph2.text, 200, 209, 60, 100)

        subjective_text = SubjectiveText(text, [section_1, section_2])

        acm_result: ICD10Result = icd10_annotation_component.run(
            {SectionExclusionServiceComponent: [],  # need to modify
             SubjectiveSectionExtractorComponent: [subjective_text],
             NotePreprocessingComponent: [[paragraph1, paragraph2], [paragraph3, paragraph4]],
             "acm_cached_result": None, "id": "123", "text": "abcd",
             NegationHandlingComponent: [
                 NegationResult(paragraph1.text + "\n\n" + paragraph2.text.replace("pneumonia", "Pneumonia")),
                 NegationResult(paragraph3.text + "\n\n" + paragraph4.text.replace("flurosemide", "Flurosemide")),
             ],
             "changed_words": {"Pneumonia": [ChangedWordAnnotation("pneumonia", "Pneumonia", 11, 20)],
                               "Flurosemide": [ChangedWordAnnotation("flurosemide", "Flurosemide", 31, 40)]}})[0]
        calls = [call("Some TEXT"), call("pneumonia some other text")]

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

        assert icd10_result[1].begin_offset == 101
        assert icd10_result[1].end_offset == 105
        assert icd10_result[1].medical_condition == "Tuberculosis"

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
        assert icd10_result[0].medical_condition == "Tuberculosis"

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
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=11,
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

        return [[icd10_annotation_result_1], [icd10_annotation_result_2]]

    def __get_dummy_icd10_data(self):
        icd10_annotation_1 = ICD10Annotation(code="A15.0", description="Tuberculosis of lung", score=0.7)
        icd10_annotation_2 = ICD10Annotation(code="A15.9", description="Respiratory tuberculosis unspecified",
                                             score=0.54)
        icd10_annotation_result_1 = ICD10AnnotationResult(medical_condition="Tuberculosis", begin_offset=11,
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

    @staticmethod
    def __mock_text_preprocessor_util_side_effect(text):
        return text + "."
