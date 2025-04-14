from typing import Optional
from engine.field.zones import FieldZone


class TacticalAction:
    def __init__(self, action_type: str, comment: str = "", target_zone: Optional[FieldZone] = None):
        self.action_type = action_type
        self.comment = comment
        self.target_zone = target_zone

    def __str__(self):
        return f"{self.action_type.upper()} | {self.comment}"

