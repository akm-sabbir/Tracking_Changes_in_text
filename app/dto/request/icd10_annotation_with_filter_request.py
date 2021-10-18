import re

from pydantic import validator, Field
from typing import Optional

from app.dto.base_dto import BaseDto


class ICD10AnnotationWithFilterRequest(BaseDto):
    text: str
    dx_threshold: Optional[float]
    icd10_threshold: Optional[float]
    parent_threshold: Optional[float]
    error_message: str = "must be floating point number"

    @validator('text')
    def text_must_be_string_and_nonempty(cls, text: str):
        if len(text.strip()) == 0 or re.match(r"[0-9.]+|true|false", text.lower()):
            raise ValueError("must be string and cannot be empty")
        return text

    @validator('dx_threshold')
    def dx_threshold_must_be_float(cls, dx_threshold: float):
        if  not type(dx_threshold).__name__ == 'float':
            raise ValueError(ICD10AnnotationWithFilterRequest.error_message)
        return dx_threshold

    @validator('icd10_threshold')
    def icd10_threshold_must_be_float(cls, icd10_threshold: float):
        if not type(icd10_threshold).__name__ == 'float':
            raise ValueError(ICD10AnnotationWithFilterRequest.error_message)
        return icd10_threshold

    @validator('parent_threshold')
    def parent_threshold_must_be_float(cls, parent_threshold: float):
        if not type(parent_threshold).__name__ == 'float':
            raise ValueError(ICD10AnnotationWithFilterRequest.error_message)
        return parent_threshold
