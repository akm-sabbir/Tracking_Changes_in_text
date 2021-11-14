import spacy
from spacy.lang.en import English

from app.util.english_dictionary import EnglishDictionary
from app.dto.core.trie_structure import Trie
from nltk.corpus import words
import json
import codecs

class Settings:
    app_name: str = "HCC API"
    dx_threshold: float
    parent_threshold: float
    icd10_threshold: float
    use_cache: bool
    eng_dict: Trie
    spacy_tokenizer: spacy.Any
    exclusion_list_path: str


    @staticmethod
    def get_settings_dx_threshold() -> float:
        return Settings.dx_threshold

    @staticmethod
    def set_settings_dx_threshold(dx_threshold: float):
        Settings.dx_threshold = dx_threshold

    @staticmethod
    def get_settings_parent_threshold() -> float:
        return Settings.parent_threshold

    @staticmethod
    def set_settings_parent_threshold(p_threshold: float):
        Settings.parent_threshold = p_threshold

    @staticmethod
    def get_settings_use_cache() -> float:
        return Settings.use_cache

    @staticmethod
    def set_settings_use_cache(caching: bool):
        Settings.use_cache = caching

    @staticmethod
    def get_settings_icd10_threshold() -> float:
        return Settings.icd10_threshold

    @staticmethod
    def set_settings_icd10_threshold(icd_threshold: float):
        Settings.icd10_threshold = icd_threshold

    @staticmethod
    def set_settings_dictionary(dictionary: Trie):
        Settings.eng_dict = dictionary

    @staticmethod
    def get_settings_dictionary():
        return Settings.eng_dict

    @staticmethod
    def set_settings_tokenizer(tokenizer: object):
        Settings.spacy_tokenizer = tokenizer

    @staticmethod
    def get_settings_tokenizer():
        return Settings.spacy_tokenizer

    @staticmethod
    def set_exclusion_dict(path_: str):
        Settings.exclusion_list_path = path_

    @staticmethod
    def get_exclusion_dict():
        with codecs.open(Settings.exclusion_list_path, mode="r",encodings="utf-8", errors="ignore") as json_file:
            return json.load(json_file)

    @staticmethod
    def start_initialize_dictionary():
        eng_dic = EnglishDictionary()
        root = Trie()
        for each_word in words.words('en'):
            eng_dic.insert_in(each_word, root)
        Settings.set_settings_dictionary(root)
        Settings.set_settings_tokenizer(English())
