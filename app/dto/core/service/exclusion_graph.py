class ExclusionGraph:
    code: str
    vote: int = 0
    neighbors: dict[str] = dict()
    degree: int = 0
