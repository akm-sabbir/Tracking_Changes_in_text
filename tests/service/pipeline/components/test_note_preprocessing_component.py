from unittest import TestCase
from unittest.mock import patch, Mock, call

from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.core.service.Tokens import TokenInfo
from app.dto.pipeline.medication_section import MedicationText
from app.dto.pipeline.subjective_section import SubjectiveText
from app.dto.pipeline.token_graph_component import GraphTokenResult
from app.dto.pipeline.tokenization_component_result import TokenizationResult
from app.service.pipeline.components.icd10_token_to_graph_generation_component import TextToGraphGenerationComponent
from app.service.pipeline.components.icd10_tokenizing_text_component import TextTokenizationComponent
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.dto.pipeline.negation_component_result import NegationResult
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent


class TestNotePreprocessingComponent(TestCase):

    @patch('app.util.encounter_note_util.EncounterNoteUtil.break_note_into_paragraphs')
    @patch('app.util.config_manager.ConfigManager.get_specific_config')
    def test__run__should_return_correct_response__given_correct_input(self, mock_get_config: Mock,
                                                                       mock_break_note_into_paragraphs: Mock):
        component = NotePreprocessingComponent()
        mock_get_config.return_value = "10"
        test_text_span_set_one_subjective_section = [
            TokenInfo(token="some", start_of_span=0, end_of_span=4, offset=0),
            TokenInfo(token="text", start_of_span=5, end_of_span=9, offset=0),
            TokenInfo(token=".", start_of_span=9, end_of_span=10, offset=0),
            TokenInfo(token="Some", start_of_span=11, end_of_span=15, offset=0),
            TokenInfo(token="other", start_of_span=16, end_of_span=21, offset=0),
            TokenInfo(token="text", start_of_span=22, end_of_span=26, offset=0),
            TokenInfo(token=".", start_of_span=26, end_of_span=27, offset=0)]
        test_text_span_set_one_medication_section = [
            TokenInfo(token="medication", start_of_span=28, end_of_span=38, offset=0),
            TokenInfo(token="text", start_of_span=39, end_of_span=43, offset=0),
            TokenInfo(token=".", start_of_span=43, end_of_span=44, offset=0),
            TokenInfo(token="Some", start_of_span=45, end_of_span=49, offset=0),
            TokenInfo(token="other", start_of_span=50, end_of_span=55, offset=0),
            TokenInfo(token="medication", start_of_span=56, end_of_span=66, offset=0),
            TokenInfo(token=".", start_of_span=66, end_of_span=67, offset=0)
        ]

        mock_return_value = [[Paragraph("some text.", 0, 10), Paragraph("Some other text.", 11, 27)],
                             [Paragraph("medication text.", 28, 43), Paragraph("Some other medication.", 45, 67)]]
        mock_break_note_into_paragraphs.side_effect = mock_return_value
        result = component.run({"text": "some text. Some other text. medication text. Some other medication.",
                                'acm_cached_result': None,
                                SubjectiveSectionExtractorComponent: [SubjectiveText("some text. Some other text.", [])],
                                MedicationSectionExtractorComponent: [MedicationText("medication text. Some other medication.", [])],
                                NegationHandlingComponent: [
                                    NegationResult(token_info_with_span=test_text_span_set_one_subjective_section),
                                    NegationResult(token_info_with_span=test_text_span_set_one_medication_section)]
                                })
        assert result[0] == mock_return_value[0]
        assert result[1] == mock_return_value[1]

        calls = [call("some text. Some other text.", 10), call("medication text. Some other medication.", 10)]

        mock_break_note_into_paragraphs.assert_has_calls(calls)
        mock_get_config.assert_called_with("acm", "char_limit")

    def test__run__should_return_empty__given_cache_present(self):
        component = NotePreprocessingComponent()
        result = component.run({"text": "some text.\n\nSome other text", 'acm_cached_result': ["some data"]})
        assert result == []

