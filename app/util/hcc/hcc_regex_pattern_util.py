import re


class HCCRegexPatternUtil:

    @staticmethod
    def get_age_sex_score_key_pattern(hcc_eligibility: str) -> re.Pattern:
        return re.compile("^" + hcc_eligibility + r"[_]?[MF][0-9]?[0-9][_].*")

    @staticmethod
    def get_orec_score_key_pattern(hcc_eligibility: str) -> re.Pattern:
        return re.compile("^" + hcc_eligibility + r"[_]OriginallyDisabled[_].*")
