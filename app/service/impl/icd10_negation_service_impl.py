from collections import defaultdict

from app.Settings import Settings
from app.service.icd10_negation_service import ICD10NegationService
from app.util.english_dictionary import EnglishDictionary


class Icd10NegationServiceImpl(ICD10NegationService):

    def __init__(self, dictionary=None):
        self.dict = Settings.get_settings_dictionary() if dictionary is None else dictionary
        self.utilize_dict = EnglishDictionary()

    def dfs_search(self, trie, word, index, one_edit_words, form_strings, dist):

        if (trie.is_word is True) and (dist <= 1) and (abs(len(word) - len(form_strings)) < 2):
            one_edit_words.add(form_strings)

        if (trie is None) or (dist > 1):
            return one_edit_words

        for key, values in trie.current_elem.items():
            one_edit_words = self.dfs_search(values, word, (index + 1) % len(word), one_edit_words,
                                             form_strings + values.word, dist + 1 if key != word[index] else dist)

            if key != word[index]:
                one_edit_words = self.dfs_search(values, word, index, one_edit_words, form_strings + values.word,
                                                 dist + 1)

        one_edit_words = self.dfs_search(trie, word, (index + 1) % len(word), one_edit_words, form_strings, dist + 1)
        return one_edit_words

    def build_one_edit_distance(self, word, index=0):
        one_edit_words = set()
        form_strings = self.dict.current_elem[word[index]].word
        one_edit_words = self.dfs_search(self.dict.current_elem[word[index]], word,
                                         index + 1, one_edit_words, form_strings, 0)
        return list(one_edit_words)

    def get_icd_10_text_negation_fixed(self, text: str) -> str:
        if text.lower().find("no") == 0 and not self.utilize_dict.is_valid_word(text.lower(), self.dict, 0):
            results = self.build_one_edit_distance(text[2:].lower(), index=0)
            results = ["no " + word for word in results] if len(results) != 0 else text.lower()
            text = ",".join(results)
        return text
