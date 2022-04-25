from typing import Optional


class TokenNode:
    is_root: bool = False
    parent_token: str = ""
    length: int = 0
    pos_list: list = []
    tacking_pos: Optional[int] = None
    sub_word: str = ""