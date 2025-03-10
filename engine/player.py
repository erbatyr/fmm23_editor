from typing import Type, Dict, List

from player_tactical_roles import TacticalRole, Poacher, BoxToBoxMidfielder
from positions import Position
from player_attributes import Attribute, Aerial, Crossing, Dribbling, Passing, Shooting, Tackling, Technique, \
    Aggression, Creativity, Decisions, Leadership, Movement, Positioning, Teamwork, Pace, Stamina, Strength


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
    position=Position.CENTRE_FORWARD,
    tactical_role=Poacher()
)

available_roles = [Poacher(), BoxToBoxMidfielder()]  # и т.д.

def suggest_best_role(player: Player, roles: List[TacticalRole]) -> TacticalRole:
    best_score = -1
    best_role = None

    for role in roles:
        if player.position not in role.suitable_positions:
            continue  # Пропускаем, если роль не подходит по позиции

        total = 0
        count = 0
        for attr_type in role.key_attributes:
            total += player.get_attribute(attr_type)
            count += 1

        if count == 0:
            continue

        score = total / count

        if score > best_score:
            best_score = score
            best_role = role

    return best_role

suggested_role = suggest_best_role(player, available_roles)
print(f"Лучшая роль для {player.full_name}: {suggested_role.name}")