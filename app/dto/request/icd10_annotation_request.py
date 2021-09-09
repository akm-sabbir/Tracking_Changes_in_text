from pydantic import Field

from app.dto.base_dto import BaseDto


class ICD10AnnotationRequest(BaseDto):
    text: str = Field(min_length=1)
