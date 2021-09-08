from typing import List

from app.dto.base_dto import BaseDto


class ICD10AnnotationResponse(BaseDto):
    icd10_annotations: List
