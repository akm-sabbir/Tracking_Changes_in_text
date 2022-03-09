import json
import os.path
from typing import Dict

from app.dto.core.umls_icd10_data import UMLSICD10Data
from app.service.cui_to_icd10_service import CUItoICD10Service
from mappings import mappings_base_path


class CUItoICD10ServiceImpl(CUItoICD10Service):

    def __init__(self):
        self.cui_to_icd10_map: Dict[str, UMLSICD10Data] = {}
        data_path = os.path.join(mappings_base_path, "cui_to_icd10_mapping.json")
        with open(data_path) as json_file:
            umls_data = json.load(json_file)
            for cui in umls_data:
                data = umls_data[cui]
                self.cui_to_icd10_map[cui] = UMLSICD10Data(data["cui"], data["concept"], data["definition"],
                                                           data["icd10"])

    def get_icd10_from_cui(self, cui: str) -> str:
        if cui in self.cui_to_icd10_map:
            return self.cui_to_icd10_map[cui].icd10
        else:
            return ""

    def get_umls_data_from_cui(self, cui: str) -> UMLSICD10Data:
        if cui in self.cui_to_icd10_map:
            return self.cui_to_icd10_map[cui]
        else:
            return UMLSICD10Data(cui, None, None, "")
