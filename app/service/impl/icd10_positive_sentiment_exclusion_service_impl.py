from typing import List

from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.icd10_positive_sentiment_exclusion_service import ICD10SentimentExclusionService
from app.settings import Settings


class ICD10SentimentExclusionServiceImpl(ICD10SentimentExclusionService):
    def __init__(self):
        super().__init__()

    def __is_not_positive_sentiment_in_icd10_annotated_text(self, icd10_annotation: ICD10AnnotationResult,
                                                            positive_sentiment_exclusion_set: set):
        if icd10_annotation.is_negated:
            return True

        text_tokens = icd10_annotation.medical_condition.split()

        for words in text_tokens:
            if words.lower() in positive_sentiment_exclusion_set:
                return False

        return True

    def get_filtered_annotations_based_on_positive_sentiment(self,
                                                             icd10_annotation_results: List[ICD10AnnotationResult]):

        positive_sentiment_exclusion_set = Settings.get_sentiments_set()

        return [icd10_annotation for icd10_annotation in icd10_annotation_results
                if self.__is_not_positive_sentiment_in_icd10_annotated_text(icd10_annotation,
                                                                            positive_sentiment_exclusion_set)]
