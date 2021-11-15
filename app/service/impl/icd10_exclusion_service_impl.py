from collections import defaultdict

from app.Settings import Settings
from app.service.icd10_exclusion_service import ICD10ExclusionService
from app.util.icd_exclusions import ICDExclusions


class Icd10ExclusionServiceImpl(ICD10ExclusionService):

    def __init__(self, exclusion_dict=Settings.get_exclusion_dict()):
        self.icd_exclusion_util = ICDExclusions(exclusion_dict)

    def get_icd_10_exclusion_service_(self, icd10_metainfo: dict) -> str:
        icd10_lists = icd10_metainfo.keys()

        for key, value in icd10_metainfo.items():
            if value.remove is False:
                exclusion_list = self.icd_exclusion_util.get_excluded_list(key, icd10_lists)
                if len(exclusion_list) > 0:
                    icd10s_to_remove = self.get_not_selected_icd10_list(key, exclusion_list, icd10_metainfo)
                    for each in icd10s_to_remove:
                        icd10_metainfo[each].remove = True
        return

    def get_exclusion_list_hccmap(self,exclusion_list):
        return

    def get_not_selected_icd10_list(self, key: str, exclusion_list: list, icd10_metainfo: dict) -> list:
        resultant_icd10s = []
        if icd10_metainfo.get(key).hcc_map is None and self.get_exclusion_list_hccmap(exclusion_list) is False:
            return []

        if icd10_metainfo.get(key).hcc_map is not None and self.get_exclusion_list_hccmap(exclusion_list) is False:
            return [key]

        if icd10_metainfo.get(key) is None and self.get_exclusion_list_hccmap(exclusion_list) is True:
            return exclusion_list

        if icd10_metainfo.get(key) is not None and self.get_exclusion_list_hccmap(exclusion_list) is True:
            return []

        return resultant_icd10s