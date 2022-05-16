from unittest import TestCase

from app.util.text_preprocessor_util import TextPreProcessorUtil


class TestTextPreprocessorUtil(TestCase):
    def test__get_preprocessed_text__should_return_preprocessed_text__given_correct_input(self):
        mock_text1 = ["ABCD", "ABCD9"]

        for text in mock_text1:
            response = TextPreProcessorUtil.get_preprocessed_text(text)

            assert response == text + ","

    def test__get_preprocessed_text__should_return_original_text__given_correct_input(self):
        mock_text1 = ["ABCD)", "ABCD,"]

        for text in mock_text1:
            response = TextPreProcessorUtil.get_preprocessed_text(text)

            assert response == text
