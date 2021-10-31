from collections import defaultdict

from app.Settings import Settings
from app.service.icd10_negation_service import ICD10NegationService


class Icd10NegationServiceImpl(ICD10NegationService):

    def __init__(self):
        self.dict = Settings.get_settings_dictionary()

    def dfs_search(self, trie, word, index, one_edit_words, form_strings, dist):

        if (trie.isWord is True) and (dist <= 1) and (abs(len(word) - len(form_strings)) < 2):
            one_edit_words.add(form_strings)

        if (len(word) == index) or (trie is None) or (dist > 1):
            return one_edit_words

        for key, values in trie.current_elem.items():
            one_edit_words = self.dfs_search(values, word, index + 1, one_edit_words, form_strings + values.word,
                                             dist + 1 if key != word[index] else dist)

            if key != word[index]:
                one_edit_words = self.dfs_search(values, word, index, one_edit_words, form_strings + values.word,
                                                 dist + 1)

        one_edit_words = self.dfs_search(trie, word, index + 1, one_edit_words, form_strings, dist + 1)
        return one_edit_words

    def build_one_edit_distance(self, word, trie, index=0):
        one_edit_words = set()
        form_strings = trie.current_elem[word[index]].word
        one_edit_words = self.dfs_search(trie.current_elem[word[index]], word, index + 1, one_edit_words, form_strings, 0)
        return list(one_edit_words)

    def get_icd_10_text_negation_fixed(self, text: str) -> str:
        return text
