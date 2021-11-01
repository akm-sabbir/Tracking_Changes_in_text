from unittest import TestCase
from unittest.mock import patch, Mock

from app.dto.core.pipeline.paragraph import Paragraph
from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.Settings import Settings
from nltk.corpus import words
from app.util.english_dictionary import EnglishDictionary
from app.util.trie_structure import Trie
from spacy.lang.en import English


class TestNegationProcesingComponent(TestCase):

    def test__run__should_return_correct_response__given_correct_input(self, ):
        word = words.words()
        root = Trie()
        eng_dict = EnglishDictionary()
        for each_word in word:
            eng_dict.insert_in(each_word, root)
        Settings.set_settings_dictionary(root)
        Settings.set_settings_tokenizer(English())
        component = NegationHandlingComponent()
        result = component.run({"text": "nodizzyness noanxity noanxieti normal nothing nobreathleessness",
                                "acm_cached_result": None})

        tokens = result.split(",")
        assert "no dizziness" in tokens
        assert "no anxiety" in tokens



