class TokenNode:
    is_root: bool = False
    parent_token: str = ""
    length: int = 0
    pos_list: list = []
    tacking_pos: int = 0
    sub_word: str = ""