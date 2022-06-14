from unittest import TestCase
from unittest.mock import patch, Mock

from app.dto.request.hcc_request_dto import HCCRequestDto
from app.service.impl.hcc_service_impl import HCCServiceImpl


class MockedHCCEngine():
    def __init__(self, version: str):
        self.version = version


class TestHCCServiceImpl(TestCase):

    @patch("app.util.config_manager.ConfigManager.get_specific_config")
    def test_hcc_service_get_hcc_risk_scores_should_return_correct_response(self,
                                                                            mock_config: Mock):
        mock_config.return_value = "23"
        service: HCCServiceImpl = HCCServiceImpl()

        request_dto = HCCRequestDto(icd_codes_list=["C770", "C9430", "C9480", "C882", "B484"], age=70, sex="F",
                                    original_reason_for_entitlement="1", medicaid=True, eligibility="INS")
        response = service.get_hcc_risk_scores(request_dto)
        assert response.aggregated_risk_score == 2.98

        assert response.hcc_maps["C770"].code == "HCC8"
        assert response.hcc_maps["C770"].score == 1.302

        assert response.hcc_maps["C9430"].code == "HCC9"
        assert response.hcc_maps["C9430"].score == 0.623

        assert response.hcc_maps["C9480"].code == "HCC9"
        assert response.hcc_maps["C9480"].score == 0.623

        assert response.hcc_maps["C882"].code == "HCC10"
        assert response.hcc_maps["C882"].score == 0.461

        assert response.hcc_maps["B484"].code == "HCC6"
        assert response.hcc_maps["B484"].score == 0.535

        assert response.demographics_score == {"INS_F70_74": 1.148, "INS_OriginallyDisabled_Femle": 0.0}
        assert response.disease_interactions_score == {}

        assert response.hcc_categories['Opportunistic Infections'] == ['HCC6']
        assert response.hcc_categories['Metastatic Cancer and Acute Leukemia'] == ['HCC8', 'HCC9', 'HCC10']
