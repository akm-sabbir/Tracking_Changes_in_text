import codecs
import json
import os
from typing import List

from injector import singleton

from app import app_base_path
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.icd10_positive_sentiment_exclusion_service import ICD10SentimentExclusionService
from app.settings import Settings
from app.util.config_manager import ConfigManager

class ICD10SentimentExclusionServiceImpl(ICD10SentimentExclusionService):
    def __init__(self):
        # self.__positive_sentiment_exclusion_set = set()
        #
        # __sentiment_exclusion_folder = ConfigManager.get_specific_config(section="sentiment_exclusion", key="list_")
        #
        # positive_sentiments_path_ = os.path.join(
        #     os.path.join(os.path.dirname(app_base_path), __sentiment_exclusion_folder), "positive_sentiments.json")
        #
        # with codecs.open(positive_sentiments_path_, mode="r", encoding="utf-8", errors="ignore") as json_file:
        #     positive_sentiments_dict = json.load(json_file)
        #     self.__positive_sentiment_exclusion_set = positive_sentiments_dict["positive_sentiments"]

        self.__positive_sentiment_exclusion_set = Settings.get_sentiments_set()

    def __is_not_positive_sentiment_in_icd10_annotated_text(self, icd10_annotation: ICD10AnnotationResult):
        if icd10_annotation.is_negated: # She is not feeling good, not feeling better. These are negated but also symptoms.
            return True

        text_tokens = icd10_annotation.medical_condition.split()

        for words in text_tokens:
            if words in self.__positive_sentiment_exclusion_set:
                return False

        return True

    def get_filtered_annotations_based_on_positive_sentiment(self,
                                                             icd10_annotation_results: List[ICD10AnnotationResult]):

        return [icd10_annotation for icd10_annotation in icd10_annotation_results
                if self.__is_not_positive_sentiment_in_icd10_annotated_text(icd10_annotation)]
