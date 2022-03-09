from unittest import TestCase
from unittest.mock import mock_open, patch

from app.service.impl.cui_to_icd10_service_impl import CUItoICD10ServiceImpl

json = """{
    "C0000727": {
        "concept": "Acute abdomen",
        "cui": "C0000727",
        "definition": "A clinical syndrome with acute abdominal pain that is severe, localized, and rapid in onset. Acute abdomen may be caused by a variety of disorders, injuries, or diseases.",
        "icd10": "R10.0"
    },
    "C0000737": {
        "concept": "Unspecified abdominal pain",
        "cui": "C0000737",
        "definition": "A disorder characterized by a sensation of marked discomfort in the abdominal region.",
        "icd10": "R10.9"
    }
}"""


class TestCUItoICD10Service(TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data=json)
    def test__get_icd10_from_cui__should_return_correct_value__given_correct_input(self, mock_file):
        service = CUItoICD10ServiceImpl()
        result = service.get_icd10_from_cui("C0000727")
        assert result == "R10.0"

        result = service.get_icd10_from_cui("C0000737")
        assert result == "R10.9"

        result = service.get_icd10_from_cui("123")
        assert result == ""

    @patch("builtins.open", new_callable=mock_open, read_data=json)
    def test__get_umls_data_from_cui__should_return_correct_value__given_correct_input(self, mock_file):
        service = CUItoICD10ServiceImpl()
        result = service.get_umls_data_from_cui("C0000727")
        assert result.icd10 == "R10.0"
        assert result.definition == "A clinical syndrome with acute abdominal pain that is severe, " \
                                    "localized, and rapid in onset. Acute abdomen may be caused by a " \
                                    "variety of disorders, injuries, or diseases."

        assert result.concept == "Acute abdomen"

        result = service.get_umls_data_from_cui("C0000737")
        assert result.icd10 == "R10.9"
        assert result.definition == "A disorder characterized by a sensation " \
                                    "of marked discomfort in the abdominal region."
        assert result.concept == "Unspecified abdominal pain"

        result = service.get_umls_data_from_cui("123")

        assert result.icd10 == ""
        assert result.definition is None
        assert result.concept is None
