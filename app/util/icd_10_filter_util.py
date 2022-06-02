from typing import List

from app.dto.pipeline.excluded_sections.family_history_excluded_section import FamilyHistorySection
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult


class ICD10FilterUtil:
    excluded_terms = ["sick"]

    @staticmethod
    def __is_icd_10_codes_not_in_excluded_sections(icd10_annotation: ICD10AnnotationResult,
                                                   family_history_excluded_sections: List[FamilyHistorySection]):

        for section in family_history_excluded_sections:
            if section.start <= icd10_annotation.begin_offset <= section.end:
                return False

        return True

    @staticmethod
    def get_filtered_annotations_based_on_excluded_sections(icd10_annotation_results: List[ICD10AnnotationResult],
                                                            family_history_excluded_sections: List[
                                                                FamilyHistorySection]):

        return [icd10_annotation for icd10_annotation in icd10_annotation_results
                if
                ICD10FilterUtil.__is_icd_10_codes_not_in_excluded_sections(icd10_annotation,
                                                                           family_history_excluded_sections)]

    @staticmethod
    def is_icd10_term_valid(annotation: ICD10AnnotationResult, dx_threshold: float):
        return annotation.is_negated is False \
               and annotation.score > dx_threshold \
               and annotation.medical_condition.lower().strip() not in ICD10FilterUtil.excluded_terms
