from app.dto.core.umls_icd10_data import UMLSICD10Data


class CUItoICD10Service:
    def get_icd10_from_cui(self, cui: str) -> str:
        raise NotImplementedError()

    def get_umls_data_from_cui(self, cui: str) -> UMLSICD10Data:
        raise NotImplementedError()