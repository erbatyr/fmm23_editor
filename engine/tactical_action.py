from typing import Optional
from engine.field.zones import FieldZone
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine.player import Player


class TacticalAction:
    def __init__(self, action_type: str, comment: str = "", target_zone: Optional[FieldZone] = None, target_player: "Player" = None):
        self.action_type = action_type
        self.comment = comment
        self.target_player = target_player
        self.target_zone = target_zone

    def __str__(self):
        return f"{self.action_type.upper()} | {self.comment}"

