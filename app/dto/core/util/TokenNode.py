class TokenNode:
    is_root: bool = False
    parent_token: str = None
    length: int = 0
    pos_list: list = []
    tacking_pos: int = 0