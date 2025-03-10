import random
from typing import List, Dict, Type

from engine.player import Player
from engine.player_attributes import *
from engine.player_tactical_roles import *
from engine.positions import Position


# Примитивный список ролей и сопоставление с позициями
ROLE_POOL = {
    Position.GOALKEEPER: Goalkeeper(),
    Position.RIGHT_BACK: FullBack(),
    Position.LEFT_BACK: FullBack(),
    Position.CENTER_BACK: CentralDefender(),
    Position.DEFENSIVE_MIDFIELDER: BallWinningMidfielder(),
    Position.CENTRAL_MIDFIELDER: AdvancedPlaymaker(),
    Position.RIGHT_WINGER: Winger(),
    Position.LEFT_WINGER: Winger(),
    Position.CENTRE_FORWARD: Poacher(),
}

# Распределение по позициям (можно адаптировать)
DEFAULT_FORMATION = [
    Position.GOALKEEPER,
    Position.RIGHT_BACK,
    Position.LEFT_BACK,
    Position.CENTER_BACK,
    Position.CENTER_BACK,
    Position.DEFENSIVE_MIDFIELDER,
    Position.CENTRAL_MIDFIELDER,
    Position.RIGHT_WINGER,
    Position.LEFT_WINGER,
    Position.CENTRE_FORWARD,
    Position.CENTRE_FORWARD,
]


FIELD_PLAYER_ATTRIBUTES = [
    Aerial, Crossing, Dribbling, Passing, Shooting, Tackling, Technique,
    Aggression, Creativity, Decisions, Leadership, Movement, Positioning,
    Teamwork, Pace, Stamina, Strength
]

GOALKEEPER_ATTRIBUTES = [
    # gk only attributes
    GKAgility, GKCommunication, GKHandling, GKKicking, GKReflexes, GKThrowing,

    # general attributes
    Aerial, Technique, Aggression, Creativity, Decisions, Leadership, Positioning, Teamwork, Pace, Stamina, Strength
]


def generate_random_attributes(key_attributes: List[Type[Attribute]], position: Position) -> Dict[Type[Attribute], Attribute]:
    attributes = {}
    if position == Position.GOALKEEPER:
        relevant_attrs = GOALKEEPER_ATTRIBUTES
    else:
        relevant_attrs = FIELD_PLAYER_ATTRIBUTES

    for attr_cls in relevant_attrs:
        if attr_cls in key_attributes:
            value = random.randint(12, 20)
        else:
            value = random.randint(5, 15)
        attributes[attr_cls] = attr_cls(value)

    return attributes



def generate_team(team_name: str) -> List[Player]:
    team = []
    for i, position in enumerate(DEFAULT_FORMATION):
        role = ROLE_POOL.get(position)
        attributes = generate_random_attributes(role.key_attributes, position)
        player = Player(
            first_name=f"{team_name}_Player_{i+1}",
            last_name="Test",
            position=position,
            attributes=attributes,
            tactical_role=role
        )
        team.append(player)
    return team


team_a = generate_team("TeamA")
team_b = generate_team("TeamB")

for player in team_a:
    print(player)