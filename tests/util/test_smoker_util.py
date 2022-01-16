from typing import List
from unittest import TestCase
from app.util.smoker_util import SmokerUtility
import spacy
from unittest.mock import patch, Mock
from tests.service.impl.dummy_smoking_pattern_decision_model import DummySciSpacyModel, Language


class SmokerUtilTest(TestCase):

    @patch('app.util.smoker_util.SmokerUtility.get_nlp_obs')
    def test_smoker_utility_should_return_true(self, mock_get_model: Mock):
        dummy_model = DummySciSpacyModel()
        mock_get_model.return_value = dummy_model.get_language()
        assert isinstance(dummy_model.get_language(),Language)
