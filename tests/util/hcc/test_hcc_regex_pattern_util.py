from unittest import TestCase
from app.util.hcc.hcc_regex_pattern_util import HCCRegexPatternUtil
import re


class TestHCCRegexPatternUtil(TestCase):
    def test_get_age_sex_score_key_pattern_should_return_correct_pattern(self):
        response = HCCRegexPatternUtil.get_age_sex_score_key_pattern(hcc_eligibility="CNA")
        assert type(response) is re.Pattern
        assert response.pattern == "^CNA[_]?[MF][0-9]?[0-9][_].*"

    def test_get_orec_score_key_pattern_should_return_correct_pattern(self):
        response = HCCRegexPatternUtil.get_orec_score_key_pattern(hcc_eligibility="CNA")
        assert type(response) is re.Pattern
        assert response.pattern == "^CNA[_]OriginallyDisabled[_].*"
