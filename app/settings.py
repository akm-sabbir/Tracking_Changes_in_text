import spacy
from scispacy.candidate_generation import LinkerPaths
from spacy.lang.en import English
from scispacy.candidate_generation import DEFAULT_PATHS, DEFAULT_KNOWLEDGE_BASES
from scispacy.linking import *

from app.util.english_dictionary import EnglishDictionary
from app.util.scispacy_custom_umls import UMLS2021KnowledgeBase
from app.util.smoker_util import SmokerUtility
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
    exclusion_dict: dict
    positive_sentiments_path: str = ""
    positive_sentiments_set: set = set()
    nlp_smoker_detector: spacy

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
    def set_positive_sentiments_path(path_: str):
        Settings.positive_sentiments_path = path_

    @staticmethod
    def get_exclusion_dict():
        return Settings.exclusion_dict

    @staticmethod
    def get_sentiments_set():
        return Settings.positive_sentiments_set

    @staticmethod
    def set_nlp_smoker_detector(nlp: spacy.Language):
        Settings.nlp_smoker_detector = nlp

    @staticmethod
    def get_nlp_smoker_detector():
        return Settings.nlp_smoker_detector

    @staticmethod
    def init_exclusion_dict():
        with codecs.open(Settings.exclusion_list_path, mode="r", encoding="utf-8", errors="ignore") as json_file:
            Settings.exclusion_dict = json.load(json_file)

    @staticmethod
    def init_positive_sentiments_set():
        with codecs.open(Settings.positive_sentiments_path, mode="r", encoding="utf-8", errors="ignore") as json_file:
            positive_sentiments_dict = json.load(json_file)
            Settings.positive_sentiments_set = set(positive_sentiments_dict["positive_sentiments"])

    @staticmethod
    def set_scispacy_custom_knowledgebase_path(ann_index_path: str, tfidf_vectorizer_path: str, tfidf_vectors_path: str,
                                               concept_aliases_list_path: str):
        custom_linker_paths_2021AB = LinkerPaths(
            ann_index=ann_index_path,
            tfidf_vectorizer=tfidf_vectorizer_path,
            tfidf_vectors=tfidf_vectors_path,
            concept_aliases_list=concept_aliases_list_path,
        )

        DEFAULT_PATHS["umls2021"] = custom_linker_paths_2021AB
        DEFAULT_KNOWLEDGE_BASES["umls2021"] = UMLS2021KnowledgeBase

    @staticmethod
    def start_initialize_dictionary():
        eng_dic = EnglishDictionary()
        root = Trie()
        for each_word in words.words('en'):
            eng_dic.insert_in(each_word, root)
        Settings.set_settings_dictionary(root)
        Settings.set_settings_tokenizer(English())
        Settings.init_exclusion_dict()

    @staticmethod
    def start_initializing_smoker_detector():
        Settings.set_nlp_smoker_detector(SmokerUtility().get_nlp_obs())
