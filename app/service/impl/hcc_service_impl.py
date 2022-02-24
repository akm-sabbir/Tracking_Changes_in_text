import logging
from typing import Dict

from hccpy.hcc import HCCEngine
from injector import singleton

from app.dto.core.service.hcc_code import HCCCode
from app.dto.request.hcc_request_dto import HCCRequestDto
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.service.hcc_service import HCCService
from app.util.hcc.hcc_regex_pattern_util import HCCRegexPatternUtil


@singleton
class HCCServiceImpl(HCCService):
    __logger = logging.getLogger(__name__)
    __hcc = HCCEngine(version="23")

    def get_hcc_risk_scores(self, hcc_request_dto: HCCRequestDto) -> HCCResponseDto:
        self.__logger.debug("hcc risk score calculated")
        response = self.__hcc.profile(dx_lst=hcc_request_dto.icd_codes_list, age=hcc_request_dto.age,
                                      sex=hcc_request_dto.sex,
                                      orec=hcc_request_dto.original_reason_for_entitlement,
                                      medicaid=hcc_request_dto.medicaid,
                                      elig=hcc_request_dto.eligibility)

        return self.__map_to_hcc_response_dto(response)

    def __map_to_hcc_response_dto(self, hccpy_response: dict) -> HCCResponseDto:
        hcc_lst = [str(value) for value in hccpy_response["hcc_map"].values()]
        hcc_scores = self.__get_hcc_scores_from_hccpy_response(hcc_lst, hccpy_response)
        demographics_score = dict()
        disease_interactions_score = dict()
        self.__set_demographics_disease_interactions_score_from_hccpy_response(hccpy_response,
                                                                               demographics_score,
                                                                               disease_interactions_score)
        hcc_maps = hccpy_response["hcc_map"]
        hcc_codes_map: Dict[str, HCCCode] = {}
        for icd10 in hcc_maps:
            hcc = hcc_maps[icd10]
            hcc_code = HCCCode(code=hcc, score=hcc_scores[hcc] if hcc in hcc_scores else 0)
            hcc_codes_map[icd10] = hcc_code

        response_dto = HCCResponseDto(hcc_maps=hcc_codes_map,
                                      demographics_score=demographics_score,
                                      disease_interactions_score=disease_interactions_score,
                                      aggregated_risk_score=hccpy_response["risk_score"],
                                      demographics_details=hccpy_response["parameters"])
        return response_dto

    @staticmethod
    def __get_hcc_scores_from_hccpy_response(hcc_lst: [], hccpy_response: dict) -> dict:
        hcc_scores = {}
        elig = hccpy_response["parameters"]["elig"]
        for hcc in hcc_lst:
            key = elig + "_" + hcc
            if key in hccpy_response["details"].keys():
                hcc_scores[hcc] = hccpy_response["details"][key]
                del hccpy_response["details"][key]
        return hcc_scores

    @staticmethod
    def __set_demographics_disease_interactions_score_from_hccpy_response(hccpy_response: dict,
                                                                          demographics_score: dict,
                                                                          disease_interactions_score: dict):
        elig = hccpy_response["parameters"]["elig"]
        for key in hccpy_response["details"].keys():
            if HCCRegexPatternUtil.get_age_sex_score_key_pattern(elig).match(key) or \
                    HCCRegexPatternUtil.get_orec_score_key_pattern(elig).match(
                    key):
                demographics_score[key] = hccpy_response["details"][key]
            else:
                disease_interactions_score[key] = hccpy_response["details"][key]
