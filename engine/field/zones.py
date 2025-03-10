from enum import Enum
from dataclasses import dataclass


class Side(Enum):
    LEFT = "Left"
    CENTER = "Center"
    RIGHT = "Right"


class ZoneType(Enum):
    ATTACK = "Attack Zone"
    PRE_ATTACK = "Pre-Attack Zone"
    CENTER = "Center Zone"
    AFTER_DEFENSE = "After-Defense Zone"
    DEFENSE = "Defense Zone"


@dataclass(frozen=True)
class FieldZone:
    zone_type: ZoneType
    side: Side

    def __str__(self):
        return f"{self.zone_type.value} - {self.side.value}"
