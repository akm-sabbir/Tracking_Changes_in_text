from unittest import TestCase
from unittest.mock import patch, Mock, call

from app.dto.core.pipeline.paragraph import Paragraph
from app.dto.pipeline.medication_section import MedicationText
from app.dto.pipeline.subjective_section import SubjectiveText
from app.service.pipeline.components.medication_section_extractor_component import MedicationSectionExtractorComponent
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.dto.pipeline.negation_component_result import NegationResult
from app.service.pipeline.components.subjective_section_extractor_component import SubjectiveSectionExtractorComponent


class TestNotePreprocessingComponent(TestCase):

    @patch('app.util.encounter_note_util.EncounterNoteUtil.break_note_into_paragraphs')
    @patch('app.util.config_manager.ConfigManager.get_specific_config')
    def test__run__should_return_correct_response__given_correct_input(self, mock_get_config: Mock,
                                                                       mock_break_into_paragraphs: Mock):
        component = NotePreprocessingComponent()
        mock_get_config.return_value = "10"
        mock_return_value = [[Paragraph("some text", 0, 10), Paragraph("some other text", 11, 21)],
                             [Paragraph("medication text", 22, 31), Paragraph("some other medication", 32, 41)]]
        mock_break_into_paragraphs.return_value = mock_return_value
        result = component.run({"text": "some text.\n\nSome other text. medication text.\n\nSome other medication.",
                                'acm_cached_result': None,
                                SubjectiveSectionExtractorComponent: [SubjectiveText("some text.\n\nSome other text.", [])],
                                MedicationSectionExtractorComponent: [MedicationText("medication text.\n\nSome other medication.", [])]})
        assert result[0] == mock_return_value
        assert result[1] == mock_return_value

        calls = [call("some text.\n\nSome other text.", 10), call("medication text.\n\nSome other medication.", 10)]

        mock_break_into_paragraphs.assert_has_calls(calls)
        mock_get_config.assert_called_with("acm", "char_limit")

    def test__run__should_return_empty__given_cache_present(self):
        component = NotePreprocessingComponent()
        result = component.run({"text": "some text.\n\nSome other text", 'acm_cached_result': ["some data"]})
        assert result == []

