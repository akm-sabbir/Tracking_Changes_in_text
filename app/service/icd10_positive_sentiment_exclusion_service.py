from abc import ABC, abstractmethod
from typing import List

from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult


class ICD10SentimentExclusionService(ABC):
    @abstractmethod
    def get_filtered_annotations_based_on_positive_sentiment(self, icd10_annotation_results: List[ICD10AnnotationResult]):
        raise NotImplementedError()
