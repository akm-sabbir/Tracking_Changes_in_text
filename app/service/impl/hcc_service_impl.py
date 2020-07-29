import logging
from injector import singleton
from hccpy.hcc import HCCEngine
import re

from app.dto.request.hcc_request_dto import HCCRequestDto
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.service.hcc_service import HCCService


def get_age_sex_score_key_pattern(hcc_eligibility: str):
    return re.compile("^" + hcc_eligibility + r"[_]?[MF][0-9]?[0-9][_].*")


def get_orec_score_key_pattern(hcc_eligibility: str):
    return re.compile("^" + hcc_eligibility + r"[_]OriginallyDisabled[_].*")


@singleton
class HCCCServiceImpl(HCCService):
    __logger = logging.getLogger(__name__)
    __hcc = HCCEngine(version="23")

    def get_hcc_risk_scores(self, hcc_request_dto: HCCRequestDto) -> HCCResponseDto:
        self.__logger.debug("hcc risk score calculated")
        response = self.__hcc.profile(dx_lst=hcc_request_dto.icd_codes_list, age=hcc_request_dto.age,
                                      sex=hcc_request_dto.sex,
                                      orec=hcc_request_dto.original_reason_for_entitlement,
                                      medicaid=hcc_request_dto.medicaid,
                                      elig=hcc_request_dto.eligibility)

        return self.__map_to_hcc_response_dto(response, hcc_request_dto.eligibility)

    def __map_to_hcc_response_dto(self, hccpy_response: dict, elig: str) -> HCCResponseDto:
        hcc_lst = [str(value) for value in hccpy_response["hcc_map"].values()]
        hcc_scores = self.__get_hcc_scores_from_hccpy_response(hcc_lst, hccpy_response)
        demographics_score = dict()
        disease_interactions_score = dict()
        self.__set_demographics_disease_interactions_score_from_hccpy_response(hccpy_response,
                                                                               demographics_score,
                                                                               disease_interactions_score)

        response_dto = HCCResponseDto(hcc_maps=hccpy_response["hcc_map"], hcc_scores=hcc_scores,
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
            key = elig+"_"+hcc
            if key in hccpy_response["details"].keys():
                hcc_scores[key] = hccpy_response["details"][key]
                del hccpy_response["details"][key]
        return hcc_scores

    @staticmethod
    def __set_demographics_disease_interactions_score_from_hccpy_response(hccpy_response: dict,
                                                                          demographics_score: dict,
                                                                          disease_interactions_score: dict):
        elig = hccpy_response["parameters"]["elig"]
        for key in hccpy_response["details"].keys():
            if get_age_sex_score_key_pattern(elig).match(key) or get_orec_score_key_pattern(elig).match(
                    key):
                demographics_score[key] = hccpy_response["details"][key]
            else:
                disease_interactions_score[key] = hccpy_response["details"][key]
