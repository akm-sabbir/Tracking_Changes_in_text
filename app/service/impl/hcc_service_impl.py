import logging
from typing import Dict, List, Set

from hccpy.hcc import HCCEngine
from injector import singleton

from app.dto.core.service.hcc_code import HCCCode
from app.dto.request.hcc_request_dto import HCCRequestDto
from app.dto.response.hcc_response_dto import HCCResponseDto
from app.service.hcc_service import HCCService
from app.util.config_manager import ConfigManager
from app.util.hcc.hcc_category_util import HCCCategoryUtil
from app.util.hcc.hcc_regex_pattern_util import HCCRegexPatternUtil


@singleton
class HCCServiceImpl(HCCService):
    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        hcc_version = ConfigManager.get_specific_config(section="hcc", key="version")
        self.__hcc = HCCEngine(version=hcc_version)
        self.hcc_util = HCCCategoryUtil()

    def get_hcc_risk_scores(self, hcc_request_dto: HCCRequestDto) -> HCCResponseDto:
        self.__logger.debug("hcc risk score calculated")
        response = self.__hcc.profile(dx_lst=hcc_request_dto.icd_codes_list, age=hcc_request_dto.age,
                                      sex=hcc_request_dto.sex,
                                      orec=hcc_request_dto.original_reason_for_entitlement,
                                      medicaid=hcc_request_dto.medicaid,
                                      elig=hcc_request_dto.eligibility)

        default_selection = response["hcc_lst"]
        hcc_to_icd10 = {}
        hcc_maps = response["hcc_map"]

        # creates a dictionary of list of ICD-10 codes with HCC codes as keys,
        # e.g. {"HCC12":["A0.2", "A30.2"]}
        for icd10 in hcc_maps:
            hcc = hcc_maps[icd10]
            if hcc in hcc_to_icd10:
                hcc_to_icd10[hcc].append(icd10)
            else:
                hcc_to_icd10[hcc] = [icd10]

        # this block of code creates a dictionary with RAF score for all HCC codes present in for all ICD-10 codes
        """ Algorithm - short explanation
            1. For each hcc code, generate a list of HCC codes excluding it's parents from the current list
            2. Generate the RAF score for the list of HCC codes
            3. Update the response object with the new RAF scores generated
            4. The final response dictionary at the end of iteration contains RAF scores for all HCC codes.
         """
        temp_hcc_map = hcc_to_icd10
        for hcc in list(hcc_to_icd10.keys()):
            parent_hcc = self.__hcc.describe_hcc(hcc)['parents']
            for parent in parent_hcc:
                if parent in temp_hcc_map:
                    temp_hcc_map.pop(parent)
            icd10_codes = [code for codelist in temp_hcc_map.values() for code in codelist]
            current_response = self.__hcc.profile(dx_lst=icd10_codes, age=hcc_request_dto.age,
                                                  sex=hcc_request_dto.sex,
                                                  orec=hcc_request_dto.original_reason_for_entitlement,
                                                  medicaid=hcc_request_dto.medicaid,
                                                  elig=hcc_request_dto.eligibility)

            response['details'].update(current_response['details'])
            hcc_set = set(response['hcc_lst'])
            hcc_set.update(current_response['hcc_lst'])
            response['hcc_lst'] = list(hcc_set)
            response['hcc_map'].update(current_response['hcc_map'])
            response['parameters'].update(current_response['parameters'])
            temp_hcc_map = hcc_to_icd10

        hcc_categories = self.__get_hcc_categories(response['hcc_lst'])
        return self.__map_to_hcc_response_dto(response, default_selection, hcc_categories)

    def __map_to_hcc_response_dto(self, hccpy_response: dict, default_selection: List[str],
                                  hcc_categories: Dict) -> HCCResponseDto:
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
                                      demographics_details=hccpy_response["parameters"],
                                      default_selection=default_selection,
                                      hcc_categories=hcc_categories)
        return response_dto

    def __get_hcc_scores_from_hccpy_response(self, hcc_lst: [], hccpy_response: dict) -> dict:
        hcc_scores = {}
        elig = hccpy_response["parameters"]["elig"]
        for hcc in hcc_lst:
            key = elig + "_" + hcc
            if key in hccpy_response["details"].keys():
                hcc_scores[hcc] = hccpy_response["details"][key]
                del hccpy_response["details"][key]
        return hcc_scores

    def __set_demographics_disease_interactions_score_from_hccpy_response(self, hccpy_response: dict,
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

    def __get_hcc_categories(self, hcc_list: List[str]) -> Dict[str, List[str]]:
        hcc_hierarchies = {}
        hcc_set = set(hcc_list)
        already_added = set()
        hcc_list.sort()
        for hcc in hcc_list:
            if hcc in already_added:
                continue
            hcc_description = self.__hcc.describe_hcc(hcc)
            children_set = set([hcc] + hcc_description['children'])
            children_present = hcc_set.intersection(children_set)
            already_added.update(children_present)
            children_list = list(children_present)
            children_list.sort()
            hcc_category = self.hcc_util.get_hcc_category(hcc)
            if hcc_category != "N/A":
                hcc_hierarchies[hcc_category] = children_list

        return hcc_hierarchies
