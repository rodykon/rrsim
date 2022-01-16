from __future__ import annotations
from enum import Enum
from typing import Tuple


class Alliance(Enum):
    RED = "RED"
    BLUE = "BLUE"


def get_alliance_color(alliance: Alliance) -> Tuple[int, int, int]:
    if alliance == Alliance.RED:
        return 255, 0, 0
    return 0, 0, 255
