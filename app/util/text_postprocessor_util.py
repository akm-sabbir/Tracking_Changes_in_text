from typing import List
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult


class TextPostProcessorUtil:
    @staticmethod
    def get_icd10_annotations_with_post_processed_text(icd10_annotation_results: List[ICD10AnnotationResult],
                                                       paragraph_text_length: int) -> List[ICD10AnnotationResult]:
        for annotation in icd10_annotation_results:
            if annotation.end_offset > paragraph_text_length and annotation.medical_condition[-1] == ",":
                annotation.end_offset -= 1
                annotation.medical_condition = annotation.medical_condition[:-1]

        return icd10_annotation_results
