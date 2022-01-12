from app.service.icd10_smoking_pattern_service import ICD10SmokingPatternDetection


class ICD10SmokingPatternDecisionImpl(ICD10SmokingPatternDetection):

    def __init__(self):
        return

    def get_smoking_pattern_decision(self, text: str) -> str:
        return "yes"