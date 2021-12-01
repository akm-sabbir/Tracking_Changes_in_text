import re

from pydantic import validator

from app.dto.base_dto import BaseDto


class ICD10AnnotationRequest(BaseDto):
    id: str
    text: str
    sex: str
    age: float

    @validator('id')
    def id_must_be_string_and_nonempty(cls, id_value: str):
        if len(id_value.strip()) == 0 or re.match(r"^true$|^false$", id_value.strip().lower()):
            raise ValueError("id must be string and cannot be empty")
        return id_value

    @validator('text')
    def text_must_be_string_and_nonempty(cls, text: str):
        if len(text.strip()) == 0 or re.match(r"^true$|^false$|^[0-9.]+$", text.strip().lower()):
            raise ValueError("text must be string and cannot be empty")
        return text

    @validator('sex')
    def sex_must_be_string_and_nonempty(cls, text: str):
        if len(text.strip()) == 0 or re.match(r"^M|F$", text.strip().lower()):
            raise ValueError("sex must be M or F")
        return text
