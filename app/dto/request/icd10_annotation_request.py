import re

from pydantic import validator

from app.dto.base_dto import BaseDto


class ICD10AnnotationRequest(BaseDto):
    id: str
    text: str

    @validator('id')
    def id_must_be_string_and_nonempty(cls, id_value: str) -> str:
        if len(id_value.strip()) == 0 or re.match(r"true|false", id_value.lower()):
            raise ValueError("id must be string and cannot be empty")
        return id_value

    @validator('text')
    def text_must_be_string_and_nonempty(cls, text: str):
        if len(text.strip()) == 0 or re.match(r".*[a-zA-Z]+", text.lower()) is None or \
                re.match(r"true|false", text.lower()):
            raise ValueError("text must be string and cannot be empty")
        return text
