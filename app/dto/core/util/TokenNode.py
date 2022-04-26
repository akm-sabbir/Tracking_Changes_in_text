from typing import Optional
from app.dto.base_dto import BaseDto


class TokenNode(BaseDto):
    is_root: bool = False
    parent_token: str = ""
    length: int = 0
    pos_list: list = []
    pos_tracking: Optional[int] = None
    sub_word: str = ""
