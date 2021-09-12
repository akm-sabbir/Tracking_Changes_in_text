from typing import List

from app.dto.base_dto import BaseDto
from app.dto.pipeline.icd10_annotation import ICD10Annotation


class ICD10AnnotationResult(BaseDto):
    medical_condition: str
    begin_offset: int
    end_offset: int
    suggested_codes: List[ICD10Annotation]
