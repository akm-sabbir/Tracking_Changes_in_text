import operator
from collections import defaultdict
from functools import partial
from typing import List

from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult
from app.service.icd10_annotation_service_with_filters import ICD10AnnotatorServiceWithFilters


def condition_check(parent_hash_code: dict, cond_operator: operator
                    , hcc_map: dict, suggested_hash_code: dict, parent_thresh: float, code: str):
    if hcc_map.get(code) is not None:
        return True
    if (parent_hash_code.__contains__(code) is True and
            cond_operator(suggested_hash_code[parent_hash_code[code][1]], parent_thresh) is True and
            cond_operator(suggested_hash_code[parent_hash_code[code][1]],
                          suggested_hash_code[code]) is True):
        return False
    return True


def generate_parents(code, score, parent_hash_code) -> dict:
    for i in range(3, len(code)):
        if parent_hash_code.__contains__(code[:i]) is True and parent_hash_code[code[:i]][0] > score:
            continue
        parent_hash_code[code[:i]] = (score, code)
    return parent_hash_code


class ICD10AnnotatorServiceWithFilterImpl(ICD10AnnotatorServiceWithFilters):

    def __init__(self):
        return

    def get_icd_10_filtered_codes(self, icd_10_entities: List[ICD10AnnotationResult],
                                  hcc_map: dict,
                                  dx_threshold: float, icd10_threshold: float,
                                  parent_threshold: float) -> List:

        icd_10_entities = self.apply_is_negated(icd_10_entities=icd_10_entities)
        icd_10_entities = self.apply_icd10_threshold(icd_10_entities=icd_10_entities,
                                                     icd_thresh=icd10_threshold,
                                                     operate=operator.gt,
                                                     hcc_map=hcc_map)

        icd_10_entities = self.apply_parent_icd_10_threshold(icd_10_entities=icd_10_entities,
                                                             parent_thresh=parent_threshold,
                                                             operate=operator.gt,
                                                             hcc_map=hcc_map)

        return icd_10_entities

    def apply_is_negated(self, icd_10_entities: List[ICD10AnnotationResult]):
        return [icd10_entity for icd10_entity in icd_10_entities if icd10_entity.is_negated is False]

    def apply_dx_threshold(self, icd_10_entities: List[ICD10AnnotationResult], dx_thresh: float, operate) -> list:
        return [icd_10_entity for icd_10_entity in icd_10_entities if operate(icd_10_entity.score, dx_thresh)]

    def apply_icd10_threshold(self, icd_10_entities: List[ICD10AnnotationResult], icd_thresh: float, operate: operator,
                              hcc_map: dict = {}) -> list:
        return [self.filter_icd10_codes(icd_10_entity, icd_thresh, operate, hcc_map)
                for icd_10_entity in icd_10_entities]

    def filter_icd10_codes(self, icd_10_entity: ICD10AnnotationResult, icd_thresh: float, operate: operator,
                           hcc_map: dict):
        icd_10_entity.suggested_codes = [entity for entity in icd_10_entity.suggested_codes
                                         if operate(entity.score, icd_thresh) or hcc_map.__contains__(entity.code)]
        return icd_10_entity

    def apply_parent_icd_10_threshold(self, icd_10_entities: List[ICD10AnnotationResult], parent_thresh: float,
                                      operate: operator, hcc_map) -> List[ICD10AnnotationResult]:
        partially_applied = partial(self.apply_parent_threshold_to_get_parent_code,
                                    parent_thresh=parent_thresh, operate=operate, hcc_map=hcc_map)
        parent_set = list(map(partially_applied, icd_10_entities))
        return parent_set

    def apply_parent_threshold_to_get_parent_code(self, icd_10_entity: ICD10AnnotationResult,
                                                  parent_thresh: float = 0.5,
                                                  operate=None, hcc_map={}):
        suggested_hash_code = defaultdict(float)
        parent_hash_code = defaultdict(float)

        for each in icd_10_entity.suggested_codes:
            suggested_hash_code[each.code] = each.score
            parent_hash_code = generate_parents(each.code, each.score, parent_hash_code)
        suggested_codes = []
        conditional_expr = partial(condition_check, parent_hash_code=parent_hash_code, cond_operator=operate,
                                   hcc_map=hcc_map, suggested_hash_code=suggested_hash_code,
                                   parent_thresh=parent_thresh)
        for suggested_code in icd_10_entity.suggested_codes:
            if conditional_expr(code=suggested_code.code) is True:
                suggested_codes.append(suggested_code)
        icd_10_entity.suggested_codes = suggested_codes
        return icd_10_entity
