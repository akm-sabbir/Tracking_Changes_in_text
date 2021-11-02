from app.util.trie_structure import Trie
from typing import List
from unittest import TestCase
from app.util.english_dictionary import EnglishDictionary


class TestEnglishDictionary(TestCase):

    def test_is_valid_word(self,):
        english_dict = EnglishDictionary()
        root = Trie()
        words = ['cricket', 'football', 'test', 'nottested']

        for each in words:
            english_dict.insert_in(each, root, index=0)
        assert english_dict.is_valid_word('cricket', root, index=0)
        assert not english_dict.is_valid_word('Cricket', root, index=0)

    def test_insert_in(self):
        english_dict = EnglishDictionary()
        root = Trie()
        words = ['cricket', 'football', 'test', 'nottested']
        for each in words:
            assert english_dict.insert_in(each, root, index=0) == len(each) - 1