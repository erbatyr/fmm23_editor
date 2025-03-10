from abc import ABC, abstractmethod
from typing import List, Type

from engine.player_attributes import Attribute, Shooting, Movement, Pace, Positioning
from engine.positions import Position


class TacticalRole(ABC):
    name: str
    suitable_positions: List[Position]
    key_attributes: List[Type[Attribute]]

    def __init__(self, name: str, suitable_positions: List[Position], key_attributes: List[Type[Attribute]]):
        self.name = name
        self.suitable_positions = suitable_positions
        self.key_attributes = key_attributes

    @abstractmethod
    def decide_action(self, player: "Player", game_context: "GameContext") -> str:
        """Роль определяет, что игрок должен делать на поле в данный момент"""
        pass


class Poacher(TacticalRole):
    def __init__(self):
        super().__init__(
            name="Poacher",
            suitable_positions=[Position.CENTRE_FORWARD],
            key_attributes=[Shooting, Movement, Pace, Positioning]
        )

    def decide_action(self, player: "Player", game_context: "GameContext") -> str:
        if game_context.ball_near_goal_area(player):
            return "Shoot"
        elif game_context.can_make_run(player):
            return "Make Run"
        else:
            return "Stay Forward"



class TargetForward(TacticalRole):
    def modify_attributes(self, player: 'Player'):
        # player.modify_attribute(Passing, 7)
        # player.modify_attribute(Creativity, 5)
        # player.modify_attribute(Pace, -2)
        pass


class Trequartista(TacticalRole):
    def modify_attributes(self, player: 'Player'):
        # player.modify_attribute(Passing, 7)
        # player.modify_attribute(Creativity, 5)
        # player.modify_attribute(Pace, -2)
        pass