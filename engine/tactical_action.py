from typing import Optional
from engine.field.zones import FieldZone


class TacticalAction:
    def __init__(self, description: str, target_zone: Optional[FieldZone] = None, comment: str = "", target_player: Optional[Player] = None):
        self.description = description
        self.target_zone = target_zone
        self.comment = comment
        self.target_player = target_player
