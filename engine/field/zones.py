from enum import Enum, auto

class FieldZone(Enum):
    DEFENSE_LEFT = auto()
    DEFENSE_CENTER = auto()
    DEFENSE_RIGHT = auto()

    AFTER_DEFENSE_LEFT = auto()
    AFTER_DEFENSE_CENTER = auto()
    AFTER_DEFENSE_RIGHT = auto()

    CENTER_LEFT = auto()
    CENTER_CENTER = auto()
    CENTER_RIGHT = auto()

    PRE_ATTACK_LEFT = auto()
    PRE_ATTACK_CENTER = auto()
    PRE_ATTACK_RIGHT = auto()

    ATTACK_LEFT = auto()
    ATTACK_CENTER = auto()
    ATTACK_RIGHT = auto()
