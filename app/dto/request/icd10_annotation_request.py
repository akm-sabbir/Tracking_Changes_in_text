import re

from pydantic import validator, Field

from app.dto.base_dto import BaseDto


class ICD10AnnotationRequest(BaseDto):
    text: str

    @validator('text')
    def text_must_be_string_and_nonempty(cls, text: str):
        if len(text) == 0 or re.match(r"[0-9.]+|true|false", text.lower()):
            raise ValueError("must be string and cannot be empty""")
        return text
