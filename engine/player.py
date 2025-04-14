from typing import Dict, Type

from engine.player_attributes import Attribute
from engine.player_tactical_roles import TacticalRole
from engine.positions import Position


class Player:
    """Игрок состоит из набора характеристик"""
    def __init__(
            self,
            position: Position,
            first_name: str,
            last_name: str,
            attributes: Dict[Type[Attribute], Attribute],
            tactical_role: TacticalRole
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.attributes = attributes
        self.tactical_role = tactical_role

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_attribute(self, attr_type: Type[Attribute]):
        return self.attributes.get(attr_type, Attribute(0)).value

    def __str__(self):
        attrs = {k.__name__: v.value for k, v in self.attributes.items()}
        return (f"{self.first_name} {self.last_name} ({self.position.value}, Role: {self.tactical_role.name}) - "
                f"Attributes: {attrs}")
