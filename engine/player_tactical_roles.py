from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Type

from fm_mine.engine.player import Player
from fm_mine.engine.player_attributes import Attribute


@dataclass
class TacticalRole:
    name: str
    suitable_positions: List[str]
    key_attributes: List[Type[Attribute]]

    def modify_attributes(self, player: Player):
        """Изменяет характеристики игрока в зависимости от роли"""
        pass



class BoxToBoxMidfielder(TacticalRole):
    def modify_attributes(self, player: Player):
        pass

class DeepLyingPlaymaker(TacticalRole):
    def modify_attributes(self, player: Player):
        # player.modify_attribute(Passing, 7)
        # player.modify_attribute(Creativity, 5)
        # player.modify_attribute(Pace, -2)
        pass