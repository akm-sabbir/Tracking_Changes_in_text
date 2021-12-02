import re
from typing import Optional

from pydantic import validator

from app.dto.base_dto import BaseDto


class ICD10AnnotationRequest(BaseDto):
    id: str
    text: str
    sex: Optional[str] = "F"
    age: Optional[float] = 70

    @validator('id')
    def id_must_be_string_and_nonempty(cls, id_value: str):
        if len(id_value.strip()) != 0 and not re.match(r"^true$|^false$", id_value.strip().lower()):
            return id_value
        raise ValueError("id must be string and cannot be empty")

    @validator('text')
    def text_must_be_string_and_nonempty(cls, text: str):
        if len(text.strip()) != 0 and not re.match(r"^true$|^false$|^[0-9.]+$", text.strip().lower()):
            return text
        raise ValueError("text must be string and cannot be empty")

    @validator('sex')
    def sex_must_be_string_and_nonempty(cls, sex: str):
        if len(sex.strip()) != 0 and re.match(r"^M$|^F$", sex.strip()):
            return sex
        raise ValueError("sex must be M or F")
