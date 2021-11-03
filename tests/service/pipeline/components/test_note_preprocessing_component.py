from unittest import TestCase
from unittest.mock import patch, Mock

from app.dto.core.pipeline.paragraph import Paragraph
from app.service.pipeline.components.note_preprocessing_component import NotePreprocessingComponent
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent


class TestNotePreprocessingComponent(TestCase):

    @patch('app.util.encounter_note_util.EncounterNoteUtil.break_note_into_paragraphs')
    @patch('app.util.config_manager.ConfigManager.get_specific_config')
    def test__run__should_return_correct_response__given_correct_input(self, mock_get_config: Mock,
                                                                       mock_break_into_paragraphs: Mock):
        component = NotePreprocessingComponent()
        mock_get_config.return_value = "10"
        mock_return_value = [Paragraph("some text", 0, 10), Paragraph("some other text", 11, 21)]
        mock_break_into_paragraphs.return_value = mock_return_value
        result = component.run({"text": "some text.\n\nSome other text", 'acm_cached_result': None,
                                NegationHandlingComponent: "some text.\n\nSome other text."})
        assert result == mock_return_value
        mock_break_into_paragraphs.assert_called_once_with("some text.\n\nSome other text.", 10)
        mock_get_config.assert_called_once_with("acm", "char_limit")

    def test__run__should_return_empty__given_cache_present(self):
        component = NotePreprocessingComponent()
        result = component.run({"text": "some text.\n\nSome other text", 'acm_cached_result': ["some data"]})
        assert result == []

