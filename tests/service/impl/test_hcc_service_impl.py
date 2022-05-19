from unittest import TestCase
from unittest.mock import patch, Mock

from app.dto.request.hcc_request_dto import HCCRequestDto
from app.service.impl.hcc_service_impl import HCCServiceImpl


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

    @staticmethod
    def describe_hcc(hcc: str):
        response = {"description": "", "parents": ["HCC12"], "children": ["HCC15"]}
        return response


class TestHCCServiceImpl(TestCase):

    @patch("app.util.config_manager.ConfigManager.get_specific_config")
    @patch("app.service.impl.hcc_service_impl.HCCCategoryUtil")
    def test_hcc_service_get_hcc_risk_scores_should_return_correct_response(self, mock_hcc_util: Mock,
                                                                            mock_config: Mock):
        mock_config.return_value = "23"
        service: HCCServiceImpl = HCCServiceImpl()

        with patch.object(service, "_HCCServiceImpl__hcc", MockedHCCEngine(version="23")):
            request_dto = HCCRequestDto(icd_codes_list=["code1", "code2"], age=70, sex="F",
                                        original_reason_for_entitlement="1", medicaid=True, eligibility="INS")
            response = service.get_hcc_risk_scores(request_dto)
            assert response.aggregated_risk_score == 2.195

            assert response.hcc_maps["I5030"].code == "HCC85"
            assert response.hcc_maps["I5030"].score == 0.204

            assert response.hcc_maps["I509"].code == "HCC85"
            assert response.hcc_maps["I509"].score == 0.204

            assert response.hcc_maps["E1169"].code == "HCC18"
            assert response.hcc_maps["E1169"].score == 0.442

            assert response.hcc_maps["I209"].code == "HCC88"
            assert response.hcc_maps["I209"].score == 0.366

            assert response.demographics_score == {"INS_F75_79": 1.013}
            assert response.disease_interactions_score == {"INS_DIABETES_CHF": 0.17}
