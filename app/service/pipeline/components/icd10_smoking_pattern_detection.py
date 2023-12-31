from typing import List

from app.service.pipeline.components.base_pipeline_component import BasePipelineComponent
from app.service.impl.icd10_smoking_pattern_decision_impl import ICD10SmokingPatternDecisionImpl
import logging
from app.dto.pipeline.smoker_condition import PatientSmokingCondition


class PatientSmokingConditionDetectionComponent(BasePipelineComponent):
    __logger = logging.getLogger(__name__)
    DEPENDS_ON = []

    def __init__(self, nlp=None):
        super().__init__()
        self.__icd10_smoking_pattern_detect_service: ICD10SmokingPatternDecisionImpl = ICD10SmokingPatternDecisionImpl(
            nlp=nlp
        )

    def run(self, annotation_results: dict) -> List[PatientSmokingCondition]:
        if annotation_results["text"] is None:
            self.__logger.error("text field is empty unable to proceed")
            raise ValueError
        _smoker = \
            self.__icd10_smoking_pattern_detect_service.get_smoking_pattern_decision(annotation_results["text"])
        return [PatientSmokingCondition(smoker=_smoker)]
