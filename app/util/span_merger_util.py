from typing import List, Set

from app.dto.pipeline.icd10_annotation import ICD10Annotation
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult


class SpanMergerUtil:
    @staticmethod
    def get_icd_10_codes_with_relevant_spans(icd10_annotations: List[ICD10AnnotationResult],
                                             no_of_components_in_algorithm: int) -> List[ICD10AnnotationResult]:
        results: List[ICD10AnnotationResult] = []

        icd10_annotations.sort(key=lambda x: x.begin_offset)
        current_index = 0

        while current_index < len(icd10_annotations):
            no_of_merged_annotations = 0
            icd10_annotation = icd10_annotations[current_index]
            end_offset = icd10_annotation.end_offset
            suggested_codes = icd10_annotation.suggested_codes
            currently_taken_components_icd10_code_set = {icd10_result.code for icd10_result in suggested_codes}

            current_components_taken = 1

            while current_components_taken < no_of_components_in_algorithm:
                if current_index + current_components_taken < len(icd10_annotations) \
                        and icd10_annotation.begin_offset <= icd10_annotations[
                    current_index + current_components_taken].begin_offset <= end_offset:

                    # Overlapping annotations will have the end_offset
                    # set to the maximum of overlapping annotations end_offset.
                    end_offset = max(icd10_annotations[current_index + current_components_taken].end_offset, end_offset)

                    # find out the unique icd10 codes from overlapping annotations.
                    filtered_icd10_codes, filtered_icd10_codes_list = SpanMergerUtil._get_unique_icd10_codes_from_same_span(
                        currently_taken_components_icd10_code_set,
                        icd10_annotations[current_index + current_components_taken].suggested_codes)

                    suggested_codes += filtered_icd10_codes
                    currently_taken_components_icd10_code_set.update(filtered_icd10_codes_list)

                    no_of_merged_annotations += 1
                    current_components_taken += 1
                else:
                    break

            icd10_annotation.end_offset = end_offset
            icd10_annotation.suggested_codes = suggested_codes

            results.append(icd10_annotation)
            current_index += no_of_merged_annotations  # increment upto indexes that have been merged.
            current_index += 1  # loop increment

        return results

    @staticmethod
    def _get_unique_icd10_codes_from_same_span(currently_held_icd10_codes_set: Set[str],
                                               taken_components_icd10_codes: List[ICD10Annotation]):

        filtered_icd10_codes: List[ICD10Annotation] = []
        filtered_icd10_codes_list: List[str] = []

        for icd10_code in taken_components_icd10_codes:
            if icd10_code.code not in currently_held_icd10_codes_set:
                filtered_icd10_codes.append(icd10_code)
                filtered_icd10_codes_list.append(icd10_code.code)

        return filtered_icd10_codes, filtered_icd10_codes_list
