from unittest import TestCase
from unittest.mock import Mock

from app.service.impl.icd10_exclusion_list_processing_service_impl import Icd10CodeExclusionServiceImpl
from app.dto.pipeline.icd10_meta_info import ICD10MetaInfo
from app.util.icd_exclusions import ICDExclusions


class MockedHCCEngine():

    def __init__(self, version: str):
        self.version = version

    @staticmethod
    def profile(dx_lst: [], age: float, sex: str, elig: str, orec: str, medicaid: bool):
        response = {"risk_score": 2.195,
                    "details": {
                        "INS_F75_79": 1.013,
                        "INS_HCC88": 0.366,
                        "INS_HCC18": 0.442,
                        "INS_HCC85": 0.204,
                        "INS_DIABETES_CHF": 0.17},
                    "hcc_lst": ["HCC88", "HCC18", "HCC85", "HCC85_gDiabetesMellit", "DIABETES_CHF"],
                    "hcc_map": {
                        "I5030": "HCC85",
                        "I509": "HCC85",
                        "E1169": "HCC18",
                        "I209": "HCC88"},
                    "parameters": {
                        "age": 75.5,
                        "sex": "F",
                        "elig": "INS",
                        "medicaid": "false",
                        "disabled": 0,
                        "origds": 0
                    }}
        return response


class TestHCCServiceImpl(TestCase):

    service: Icd10CodeExclusionServiceImpl
    icd10_exclusion_dict: dict = {"A04": ["A05-", "A1832"], "A05": ["A404-", "A32-", "T61-T62", "A040-A044", "A02-"],
                           "A06": ["A07-"], "A08": ["J09X3", "J102", "J112"], "A09": ["K529", "R197"],
                                  "A30": ["B92"],
                                  "A32": ["P372"],
                                  "A35": ["A34", "A33"],
                                  "A40": ["P360-P361", "O85", "A4181"],
                                  "A41": ["A40-", "O85", "R7881", "P36-"], "A42": ["B471"], "A46": ["O8689"],
                                  "A48": ["B471"],
                                  "A49": ["A699", "A749", "B95-B96", "A799", "A399"], "A56": ["P391", "P231"],
                                  "A71": ["B940"],
                                  "A74": ["M023-", "A55-A56", "P391", "P231"], "A75": ["A7981"],
                                  "A85": ["B262", "A872", "B258", "B004", "G933", "B020", "B100-", "B050", "A80-"]}

    def test_icd10_exclusion_service_to_get_response(self):
        exclusion_util = ICDExclusions(exclusions_json_dict=self.icd10_exclusion_dict)
        self.service = Icd10CodeExclusionServiceImpl(exclusion_util)
        icd101 = Mock(ICD10MetaInfo)
        icd101.hcc_map = "HCC85"
        icd101.score = 0.80
        icd101.length = 5
        icd101.entity_score = 0.99
        icd101.remove = False
        icd102 = Mock(ICD10MetaInfo)
        icd102.hcc_map = "HCC85"
        icd102.score = 0.67
        icd102.length = 6
        icd102.entity_score = 0.99
        icd102.remove = False
        icd103 = Mock(ICD10MetaInfo)
        icd103.hcc_map = "HCC85"
        icd103.score = 0.71
        icd103.length = 4
        icd103.entity_score = 0.91
        icd103.remove = False
        icd104 = Mock(ICD10MetaInfo)
        icd104.hcc_map = "HCC85"
        icd104.score = 0.82
        icd104.length = 3
        icd104.entity_score = 0.99
        icd104.remove = False
        icd105 = Mock(ICD10MetaInfo)
        icd105.hcc_map = "HCC85"
        icd105.score = 0.87
        icd105.length = 5
        icd105.entity_score = 0.99
        icd105.remove = False
        icd106 = Mock(ICD10MetaInfo)
        icd106.hcc_map = ""
        icd106.score = 0.87
        icd106.length = 5
        icd106.entity_score = 0.99
        icd106.remove = False
        icd107 = Mock(ICD10MetaInfo)
        icd107.hcc_map = ""
        icd107.score = 0.81
        icd107.length = 3
        icd107.entity_score = 0.99
        icd107.remove = False
        param = {"A0531": icd101, "A40421": icd102, "A853": icd103, "A04": icd104, "A7421": icd105, "A852": icd106,
                 "A32": icd107}
        param = self.service.get_icd_10_code_exclusion_decision(param)
        assert param["A0531"].remove == True
        assert param["A40421"].remove == True
        assert self.service.get_exclusion_list_hccmap(["A04"], param) is True
        assert self.service.get_exclusion_list_hccmap(["A852"], param) is False
        assert self.service.get_decision_on_choice(param, "A40421", ["A0531", "A852"])[0] == "A0531"
        assert self.service.get_decision_on_choice(param, "A40421", ["A0531", "A852"])[1] == "A852"
        assert self.service.get_decision_on_choice(param, "A0531", ["A852"])[0] == "A0531"
        assert self.service.get_decision_on_choice(param, "A852", ["A0531"])[0] == "A0531"
        assert self.service.get_decision_on_choice(param, "A04", ["A32"])[0] == "A04"
        assert len(self.service.get_decision_on_choice(param, "A853", ["A853", "A852"])) > 1
        assert self.service.get_not_selected_icd10_list("A40421", ["A0531", "A852"], param)[0] == "A0531"
        assert self.service.get_not_selected_icd10_list("A40421", ["A0531", "A32"], param)[0] == "A40421"
        assert self.service.get_not_selected_icd10_list("A40421", ["A0531", "A04"], param)[0] == "A0531"
        assert self.service.get_not_selected_icd10_list("A40421", ["A852", "A32"], param)[0] == "A40421"