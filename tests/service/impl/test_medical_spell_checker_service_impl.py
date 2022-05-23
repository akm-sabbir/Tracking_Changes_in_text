from unittest import TestCase
from unittest.mock import patch, Mock

from symspellpy import SymSpell
from symspellpy.suggest_item import SuggestItem

from app.service.impl.medical_spell_checker_service_impl import MedicalSpellCheckerServiceImpl


class TestMedicalSpellCheckerServiceImpl(TestCase):
    @patch("app.service.impl.medical_spell_checker_service_impl.pkg_resources.resource_filename")
    @patch("app.service.impl.medical_spell_checker_service_impl.SymSpell")
    def test__get_corrected_text__given_correct_input__should_return_corrected_text(self,
                                                                                    mock_symspell: Mock,
                                                                                    mock_pkg_resource: Mock):
        mock_sentence = "shebreathing"
        mock_spell = Mock(SymSpell)
        mock_spell.lookup_compound.return_value = self._get_mock_suggest_item()
        mock_symspell.return_value = mock_spell
        mock_pathname = "mock path"
        mock_pkg_resource.return_value = mock_pathname

        medical_spell_checker = MedicalSpellCheckerServiceImpl(0, 7)

        result_text = medical_spell_checker.get_corrected_text(mock_sentence, 0, True, True, True, True)

        mock_symspell.assert_called()
        mock_symspell.assert_called_once_with(0, 7)

        mock_pkg_resource.assert_called()

        mock_spell.load_dictionary.assert_called_once_with(mock_pathname, 0, 1)
        mock_spell.load_bigram_dictionary.assert_called_once_with(mock_pathname, term_index=0, count_index=2)

        mock_spell.lookup_compound.assert_called()
        mock_spell.lookup_compound.assert_called_once_with(mock_sentence,
                                                           max_edit_distance=0, transfer_casing=True,
                                                           ignore_non_words=True, split_by_space=True,
                                                           ignore_term_with_digits=True)

        assert result_text == "she breathing"

    def _get_mock_suggest_item(self):
        mock_suggest_item = [Mock(SuggestItem)]

        mock_suggest_item[0].term = "she breathing"

        return mock_suggest_item
