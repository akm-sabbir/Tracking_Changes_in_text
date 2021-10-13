from abc import abstractmethod, ABC
from typing import List

from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.exception.service_exception import ServiceException
from app.service.icd10_annotator_service_with_filters import ICD10AnnotatorServiceWithFilter
import operator
from functools import partial
from collections import defaultdict


class ICD10AnnotatorServiceWithFilterImpl(ICD10AnnotatorServiceWithFilter):

    def get_icd_10_filtered_codes(self, icd_10_entities: list[ICD10AnnotationResult],
                                  dx_threshold: float, icd10_threshod: float,
                                  parent_threshold: float) -> List:
        icd_10_entities = self.apply_dx_threshold(icd_10_entities=icd_10_entities, dx_thresh=dx_threshold,
                                                  operate=operator.gt)
        icd_10_entities = self.apply_icd10_threshold(icd_10_entities=icd_10_entities,
                                                     icd_thresh=icd10_threshod,
                                                     operate=operator.gt)
        return icd_10_entities

    def apply_dx_threshold(self, icd_10_entities: list[ICD10AnnotationResult], dx_thresh: float, operate) -> list:
        return [icd_10_entity for icd_10_entity in icd_10_entities if operate(icd_10_entity.score, dx_thresh)]

    def apply_icd10_threshold(self, icd_10_entities: list[ICD10AnnotationResult], icd_thresh: float, operate) -> list:
        return [self.filter_icd10_codes(icd_10_entity, icd_thresh, operate)
                for icd_10_entity in icd_10_entities]

    def filter_icd10_codes(self, icd_10_entity: ICD10AnnotationResult, icd_thresh: float, operate):
        icd_10_entity.suggested_codes = [entity for entity in icd_10_entity.suggested_codes
                                         if operate(entity.score, icd_thresh)]
        return icd_10_entity

    def get_parent_icd_10_code(self, icd_10_entities: list[ICD10AnnotationResult], parent_thresh: float, operate):
        partially_applied = partial(self.apply_parent_threshold_to_get_parent_code(
            parent_thresh=parent_thresh, operate=operate))
        parent_set = map(partially_applied, icd_10_entities)
        return parent_set

    def apply_parent_threshold_to_get_parent_code(self, icd_10_entity: ICD10AnnotationResult,
                                                  parent_thresh: float = 0.5,
                                                  operate=None):
        suggested_hash_code = defaultdict(float)
        parent_hash_code = defaultdict(float)

        def generate_parents(code, score, parent_hash_code):
            for i in range(3, len(code)):
                parent_hash_code[code[:i]] = score
        for each in icd_10_entity.suggested_codes:
            suggested_hash_code[each.code] = each.score
            generate_parents(each.code, each.score, parent_hash_code)
