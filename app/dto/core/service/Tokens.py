from app.dto.base_dto import BaseDto


class TokenInfo(BaseDto):
    token: str
    start_of_span: int
    end_of_span: int
    offset: int = 0
