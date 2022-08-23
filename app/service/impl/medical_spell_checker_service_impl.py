from typing import List

import spacy
from medcat.cdb import CDB
from medcat.config import Config
from medcat.utils.normalizers import BasicSpellChecker
from medcat.vocab import Vocab

from app.service.spell_checker_service import SpellCheckerService
from app.util.config_manager import ConfigManager


class MedicalSpellCheckerServiceImpl(SpellCheckerService):
    def __init__(self, cdb_vocab: CDB, config: Config, data_vocab: Vocab):
        self.__model_name = ConfigManager.get_specific_config("scispacy_umls_model_name", "umls_model_name")

        self._medical_spell_checker = BasicSpellChecker(cdb_vocab.vocab, config, data_vocab.vocab)

        self.nlp = spacy.load(self.__model_name)

    def get_corrected_text(self, sentence: str) -> List[tuple]:
        spacy_doc = self.nlp(sentence)

        return [(token.text, self._medical_spell_checker.fix(token.lower_)) for token in spacy_doc if token.is_alpha]
