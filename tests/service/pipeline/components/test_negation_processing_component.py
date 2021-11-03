from unittest import TestCase

from app.service.pipeline.components.negation_processing_component import NegationHandlingComponent
from app.Settings import Settings
from nltk.corpus import words
from app.util.english_dictionary import EnglishDictionary
from app.dto.core.trie_structure import Trie
from spacy.lang.en import English
import time


class TestNegationProcesingComponent(TestCase):

    def test__run__should_return_correct_response__given_correct_input(self, ):
        start_time = time.time()
        word = ["dizziness", "anxiety", "appropriate", "breathlessness", "normal", "nothing"]
        root = Trie()
        eng_dict = EnglishDictionary()
        for each_word in word:
            eng_dict.insert_in(each_word, root)
        Settings.set_settings_dictionary(root)
        Settings.set_settings_tokenizer(English())
        print("--- %s seconds ---" % (time.time() - start_time))
        component = NegationHandlingComponent()
        start_time = time.time()
        result = component.run({"text": "nodizzyness, noanxieety, noanxieti, noanxiet, normal nothing, nobreathlessnes",
                                "acm_cached_result": None})
        print("--- %s seconds ---" % (time.time() - start_time))
        print(result)
        tokens = result[0].split(", ")
        assert "no dizziness" in tokens
        assert "no anxiety" in tokens



