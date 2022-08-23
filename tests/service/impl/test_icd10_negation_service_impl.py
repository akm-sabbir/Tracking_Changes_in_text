from unittest import TestCase

from app.service.impl.icd10_negation_service_impl import Icd10NegationServiceImpl
from app.settings import Settings
from nltk.corpus import words
from app.util.english_dictionary import EnglishDictionary
from app.dto.core.trie_structure import Trie


class TestIcd10NegationServiceImpl(TestCase):
    word = ["dizziness", "anxiety", "appropriate", "breathlessness", "pail", "groom", "groot"]
    eng_dict = EnglishDictionary()
    root = Trie()
    for each_word in word:
        eng_dict.insert_in(each_word, root)
    Settings.set_settings_dictionary(root)
    __fixing_dictionary_object = Icd10NegationServiceImpl(Settings.get_settings_dictionary())

    def test__get_icd_10_negation_fixed_codes__should_return_correct_value__given_correct_text(self, ):
        test_set = ["nodizzyness", "noanxity", "noapproepriate"]
        result_sets = self.__fixing_dictionary_object.get_icd_10_text_negation_fixed(test_set[0])
        print(result_sets)
        assert result_sets[0][1] == "no" and result_sets[1][1] == "dizziness"
        result_sets = self.__fixing_dictionary_object.get_icd_10_text_negation_fixed(test_set[1])
        assert result_sets[0][1] == "no" and result_sets[1][1] == "anxiety"
        result_sets = self.__fixing_dictionary_object.get_icd_10_text_negation_fixed(test_set[2])
        assert result_sets[0][1] == "no" and result_sets[1][1] == "appropriate"

    def test__get_icd_10_negation_fixed_codes_should_return_suggested_text(self, ):
        test_set = ["nodizzyness", "nopain"]
        result_sets = self.__fixing_dictionary_object.get_icd_10_text_negation_fixed(test_set[0])
        assert result_sets[0][1] == "no" and  result_sets[1][1] == "dizziness"
        result_sets = self.__fixing_dictionary_object.get_icd_10_text_negation_fixed(test_set[1])
        assert result_sets[0][1] == "no" and result_sets[1][1] == "pail"

    def test__get_icd_10_negation_fixed_codes_should_return_unchanged_text(self, ):
        test_set = ["nodizzyness", "nochain"]
        result_sets = self.__fixing_dictionary_object.get_icd_10_text_negation_fixed(test_set[0])
        assert result_sets[0][1] == "no" and result_sets[1][1] == "dizziness"
        result_sets = self.__fixing_dictionary_object.get_icd_10_text_negation_fixed(test_set[1])
        assert result_sets[0][1] == "nochain"

    def test_get_icd_10_negation_fixed_codes_should_return_multiple_suggestions(self):
        test_set = ["nodizzyness", "nogrook"]
        result_sets = self.__fixing_dictionary_object.get_icd_10_text_negation_fixed(test_set[0])
        assert result_sets[0][1] == "no" and result_sets[1][1] == "dizziness"
        result_sets = self.__fixing_dictionary_object.get_icd_10_text_negation_fixed(test_set[1])
        assert result_sets[0][1] == "nogrook"

    def test_get_icd_10_negation_fixed_codes_should_return_multiple_suggestions(self):
        test_set = ["nodizzyness", "nogrook"]
        result_sets = self.__fixing_dictionary_object.get_icd_10_text_negation_fixed(test_set[0])
        assert result_sets[0][1] == "no" and result_sets[1][1] == "dizziness"
        result_sets = self.__fixing_dictionary_object.get_icd_10_text_negation_fixed(test_set[1])
        assert result_sets[0][1] == "nogrook"

    def __get_dummy_icd10_response(self):
        return
