from typing import Type, Dict

from fm_mine.engine.positions import Position
from fm_mine.engine.player_attributes import Attribute, Aerial, Crossing, Dribbling, Passing, Shooting, Tackling, Technique, \
    Aggression, Creativity, Decisions, Leadership, Movement, Positioning, Teamwork, Pace, Stamina, Strength


class Player:
    """Игрок состоит из набора характеристик"""
    def __init__(self, position: Position, first_name: str, last_name: str, attributes: Dict[Type[Attribute], Attribute]):
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.attributes = attributes

    def get_attribute(self, attr_type: Type[Attribute]):
        return self.attributes.get(attr_type, Attribute(0)).value

    def modify_attribute(self, attr_type: Type[Attribute], amount: int):
        """Изменяет характеристику игрока"""
        if attr_type in self.attributes:
            self.attributes[attr_type].modify(amount)

    def __str__(self):
        attrs = {k.__name__: v.value for k, v in self.attributes.items()}
        return f"{self.first_name} {self.last_name} ({self.position}) - Attributes: {attrs}"


player_attributes = {
    Aerial: Aerial(9),
    Crossing: Crossing(12),
    Dribbling: Dribbling(13),
    Passing: Passing(14),
    Shooting: Shooting(14),
    Tackling: Tackling(7),
    Technique: Technique(18),
    Aggression: Aggression(11),
    Creativity: Creativity(14),
    Decisions: Decisions(14),
    Leadership: Leadership(8),
    Movement: Movement(16),
    Positioning: Positioning(7),
    Teamwork: Teamwork(15),
    Pace: Pace(13),
    Stamina: Stamina(9),
    Strength: Strength(10)
}
player = Player(
    first_name='Sergei',
    last_name='Miroshnichenko',
    attributes=player_attributes,
    position=Position.CENTRE_FORWARD
)

