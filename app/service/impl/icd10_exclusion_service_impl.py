from collections import defaultdict

from app.Settings import Settings
from app.service.icd10_exclusion_service import ICD10ExclusionService
from app.util.icd_exclusions import ICDExclusions


class Icd10ExclusionServiceImpl(ICD10ExclusionService):

    def __init__(self, exclusion_dict=Settings.get_exclusion_dict()):
        self.icd_exclusion_util = ICDExclusions(exclusion_dict)

    def get_icd_10_exclusion_service_(self, icd_data_dict: dict) -> str:
        return
