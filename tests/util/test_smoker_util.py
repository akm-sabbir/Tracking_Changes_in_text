from typing import List
from unittest import TestCase
from app.util.smoker_util import SmokerUtility
import spacy


class SmokerUtilTest(TestCase):

    def test_smoker_utility_should_return_true(self):
        nlp_object = SmokerUtility.get_nlp_obs()
        assert isinstance(nlp_object, spacy.Language) is True
