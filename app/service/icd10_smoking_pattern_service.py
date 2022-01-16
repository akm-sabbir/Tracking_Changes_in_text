from abc import ABC, abstractmethod
from typing import List

from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult


class ICD10SmokingPatternDetection(ABC):
    @abstractmethod
    def get_smoking_pattern_decision(self, text: str) -> bool:
        raise NotImplementedError()
