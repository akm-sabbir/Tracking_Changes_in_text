from unittest import TestCase

from app.util.text_preprocessor_util import TextPreprocessorUtil


class TestTextPreprocessorUtil(TestCase):
    def test__get_preprocessed_text__should_return_preprocessed_text__given_correct_input(self):
        mock_text1 = "ABCD"

        response = TextPreprocessorUtil.get_preprocessed_text(mock_text1)

        assert response == "ABCD."

