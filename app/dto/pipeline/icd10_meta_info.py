from dataclasses import dataclass


@dataclass
class icd10_meta_info:
    hcc_map: str = None
    score: float = 0.0
    entity_score: float = 0.0
    length: int = 0
    remove: bool = False
