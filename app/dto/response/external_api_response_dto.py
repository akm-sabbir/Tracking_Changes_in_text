from app.dto.base_dto import BaseDto


class ExternalApiResponseDto(BaseDto):
    user_id: str
    id: str
    title: str
    body: str
