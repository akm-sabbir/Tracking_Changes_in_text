from unittest import TestCase
from unittest.mock import patch, Mock

from medcat.cdb import CDB
from medcat.config import Config
from medcat.utils.normalizers import BasicSpellChecker
from medcat.vocab import Vocab
from spacy.lang.en import English
from spacy.tokens import Doc

from app.service.impl.medical_spell_checker_service_impl import MedicalSpellCheckerServiceImpl


class TestMedicalSpellCheckerServiceImpl(TestCase):
    @patch('app.service.impl.medical_spell_checker_service_impl.ConfigManager.get_specific_config', Mock())
    @patch('app.service.impl.medical_spell_checker_service_impl.spacy.load')
    def test__get_corrected_text__given_correct_input__should_return_corrected_text(self, mock_nlp: Mock):
        mock_nlp.return_value = self.__get_dummy_spacy_object()

        mock_cdb_vocab = Mock(CDB)
        mock_config = Mock(Config)
        mock_data_vocab = Mock(Vocab)

        mock_cdb_vocab.vocab = Mock()
        mock_data_vocab.vocab = Mock()

        mock_spell_checker = Mock(BasicSpellChecker)
        mock_spell_checker.fix = Mock()
        mock_spell_checker.fix.side_effect = self.__get_dummy_spell_fixing_results()

        medical_spell_checker_service = MedicalSpellCheckerServiceImpl(mock_cdb_vocab, mock_config, mock_data_vocab)

        medical_spell_checker_service._medical_spell_checker = mock_spell_checker

        mock_sentence = "ome 225,"

        result = medical_spell_checker_service.get_corrected_text(mock_sentence)

        assert result[0] == ("ome", "some")
        assert result[1] == ("a225", None)

    def __get_dummy_spacy_object(self):
        mock_doc1 = Mock(Doc)
        mock_doc1.text = "ome"
        mock_doc1.lower_ = "ome"
        mock_doc1.is_alpha = True

        mock_doc2 = Mock(Doc)
        mock_doc2.text = "a225"
        mock_doc2.lower_ = "a225"
        mock_doc2.is_alpha = True

        mock_doc3 = Mock(Doc)
        mock_doc3.text = ","
        mock_doc3.lower_ = ","
        mock_doc3.is_alpha = False

        mock_nlp = Mock(English)
        mock_nlp.return_value = [mock_doc1, mock_doc2, mock_doc3]

        return mock_nlp

    def __get_dummy_spell_fixing_results(self):
        return ["some", None]
