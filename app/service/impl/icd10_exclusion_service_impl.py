from collections import defaultdict
from app.service.icd10_exclusion_service import ICD10ExclusionService
from app.util.icd_exclusions import ICDExclusions
import math
from app.Settings import Settings


class Icd10ExclusionServiceImpl(ICD10ExclusionService):
    icd_exclusion_util: ICDExclusions = ICDExclusions()

    def get_icd_10_exclusion_service_(self, icd10_metainfo: dict) -> dict:
        if self.icd_exclusion_util.exclusion_dictionary is None:
            self.icd_exclusion_util.set_exclusion_dictionary(Settings.get_exclusion_dict())
        icd10_lists = icd10_metainfo.keys()

        for key, value in icd10_metainfo.items():
            if value.remove is False:
                exclusion_list = self.icd_exclusion_util.get_excluded_list(key, icd10_lists)
                if len(exclusion_list) > 0:
                    icd10s_to_remove = self.get_not_selected_icd10_list(key, exclusion_list, icd10_metainfo)
                    for each in icd10s_to_remove:
                        icd10_metainfo[each].remove = True
        return icd10_metainfo

    def get_exclusion_list_hccmap(self, exclusion_list: list, meta_info: dict):
        for each_elem in exclusion_list:
            if meta_info.get(each_elem) is not None and meta_info.get(each_elem).hcc_map is not None:
                return True
        return False

    def get_avg_acm_score(self, exclusion_list: list, icd10_metainfo: dict):
        scores = [icd10_metainfo[elem].score for elem in exclusion_list]
        return sum(scores) / len(scores)

    def get_avg_acm_icd10code_len(self, exclusion_list: list):
        return sum([len(element) for element in exclusion_list]) / len(exclusion_list)

    def get_decision_on_choice(self, icd10_metainfo: dict, key: str, exclusion_list: list):
        if (math.fabs(
                icd10_metainfo.get(key).score - self.get_avg_acm_score(exclusion_list, icd10_metainfo)) > 0.15):
            if icd10_metainfo.get(key).score > self.get_avg_acm_score(exclusion_list, icd10_metainfo):
                return [key]
            else:
                return exclusion_list
        if len(key) > self.get_avg_acm_icd10code_len(exclusion_list):
            return [key]
        if len(key) < self.get_avg_acm_icd10code_len(exclusion_list):
            return exclusion_list
        if len(exclusion_list) > 1:
            return exclusion_list
        if icd10_metainfo.get(key).score > icd10_metainfo.get(exclusion_list[0]).score:
            return [key]
        else:
            return exclusion_list

    def get_not_selected_icd10_list(self, key: str, exclusion_list: list, icd10_metainfo: dict) -> list:
        if icd10_metainfo.get(key).hcc_map is None and \
                self.get_exclusion_list_hccmap(exclusion_list, icd10_metainfo) is False:
            return self.get_decision_on_choice(icd10_metainfo, key, exclusion_list)

        if icd10_metainfo.get(key).hcc_map is not None and \
                self.get_exclusion_list_hccmap(exclusion_list, icd10_metainfo) is False:
            return [key]

        if icd10_metainfo.get(key).hcc_map is None and \
                self.get_exclusion_list_hccmap(exclusion_list, icd10_metainfo) is True:
            return exclusion_list

        if icd10_metainfo.get(key).hcc_map is not None and \
                self.get_exclusion_list_hccmap(exclusion_list, icd10_metainfo) is True \
                and len(exclusion_list) > 1 and sum(
            [1 if icd10_metainfo.get(each_elem).hcc_map is not None else 0 for each_elem in exclusion_list]) \
                > 1:
            return exclusion_list

        return self.get_decision_on_choice(icd10_metainfo, key, exclusion_list)
