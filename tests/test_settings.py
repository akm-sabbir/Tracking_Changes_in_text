from unittest import TestCase
from unittest.mock import Mock, patch

from app.settings import Settings


class TestSettings(TestCase):

    def test_configuration_values_should_return_correct_output(self):
        Settings.set_settings_dx_threshold(0.9)
        Settings.set_settings_icd10_threshold(0.67)
        Settings.set_settings_use_cache(True)
        Settings.set_settings_parent_threshold(0.8)
        assert Settings.get_settings_dx_threshold() == 0.9
        assert Settings.get_settings_icd10_threshold() == 0.67
        assert Settings.get_settings_use_cache() == True
        assert Settings.get_settings_parent_threshold() == 0.8

    @patch.object(Settings, "positive_sentiments_set", new={"abc"})
    def test_positive_sentiment_should_return_correct_output(self):
        assert Settings.get_sentiments_set() == {"abc"}

    @patch.object(Settings, "positive_sentiments_path", new="path")
    @patch("codecs.open")
    @patch("json.load")
    def test_init_positive_sentiments_set__given_correct_input__should_assign_correct_output(self, mock_json: Mock, mock_open: Mock):
        mock_json.return_value = {"positive_sentiments": ["abc"]}

        Settings.init_positive_sentiments_set()

        mock_open.assert_called_once()
        mock_open.assert_called_once_with("path", mode="r", encoding="utf-8", errors="ignore")

        assert Settings.positive_sentiments_set == {"abc"}

    def test_set_positive_sentiments_path__given_correct_input__assign_correct_oath(self):
        Settings.set_positive_sentiments_path("path")

        assert Settings.positive_sentiments_path == "path"
