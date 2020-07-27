from pydantic import Field

from app.dto.base_dto import BaseDto


class ExternalApiPostRequestDto(BaseDto):
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
