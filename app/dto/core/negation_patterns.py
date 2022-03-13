from enum import Enum
from typing import List


class NegationPatterns(Enum):
    PRECEDING_NEGATIONS: List[str] = ['deny', 'refuse', 'neither', 'nor']
    FOLLOWING_NEGATIONS: List[str] = ['absent', 'deny', 'decline']
