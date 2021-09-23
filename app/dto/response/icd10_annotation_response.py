from typing import List

from app.dto.base_dto import BaseDto
from app.dto.pipeline.icd10_annotation_result import ICD10AnnotationResult


class ICD10AnnotationResponse(BaseDto):
    icd10_annotations: List[ICD10AnnotationResult]
