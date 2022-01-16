from typing import List
from unittest import TestCase

from app.util import smoker_information_parser
from app.util.smoker_information_parser import SmokerInfoParser


class SmokerInformationParserTest(TestCase):
    smoker_info_parsing: SmokerInfoParser

    def test_smoker_information_parsing_should_match_the_text(self):
        self.smoker_info_parsing = SmokerInfoParser()
        returned_text = self.smoker_info_parsing.get_parsed_info("Was the patient queried about smoking behavior? Yes No\n"
                                            "Does the patient currently smoke? . (Smoking Hx).")
        assert returned_text == ". (smoking hx)."
        returned_text = self.smoker_info_parsing.get_parsed_info("as the patient queried about smoking behavior? Yes No\n"
        "Does the patient currently smoke? Smoking: Patient has never smoked - (1/21/2020).\n")
        assert returned_text == "patient has never smoked - (1/21/2020)."