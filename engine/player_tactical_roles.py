from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Type

from engine.field.zones import ZoneType
from engine.player_attributes import Attribute, GKReflexes, GKHandling, GKCommunication, GKAgility, Positioning, \
    Tackling, Crossing, Pace, Stamina, Strength, Aerial, Decisions, Aggression, Teamwork, Passing, Creativity, \
    Technique, Movement, Dribbling, Shooting
from engine.positions import Position
from engine.tactical_action import TacticalAction


@dataclass
class TacticalRole(ABC):
    name: str
    suitable_positions: List[Position]
    key_attributes: List[Type[Attribute]]

    @abstractmethod
    def behave(self, player, zone_analyzer, current_zone) -> TacticalAction:
        pass


class Goalkeeper(TacticalRole):
    def __init__(self):
        super().__init__(
            name="Goalkeeper",
            suitable_positions=[Position.GOALKEEPER],
            key_attributes=[GKReflexes, GKHandling, GKCommunication, GKAgility, Positioning]
        )

    def behave(self, player, zone_analyzer, current_zone) -> TacticalAction:
        if current_zone.zone_type == ZoneType.DEFENSE:
            return TacticalAction("hold", comment="контролирует мяч и анализирует розыгрыш")
        target_zone = zone_analyzer.get_zone_by_type(ZoneType.DEFENSE, current_zone.side)
        return TacticalAction("move", target_zone=target_zone, comment="возвращается в ворота")


class FullBack(TacticalRole):
    def __init__(self):
        super().__init__(
            name="Full-Back",
            suitable_positions=[Position.RIGHT_BACK, Position.LEFT_BACK],
            key_attributes=[Tackling, Positioning, Crossing, Pace, Stamina]
        )

    def behave(self, player, zone_analyzer, current_zone) -> TacticalAction:
        if current_zone.zone_type == ZoneType.PRE_ATTACK:
            return TacticalAction("cross", comment="готовит навес в штрафную")
        target_zone = zone_analyzer.get_zone_by_type(ZoneType.PRE_ATTACK, current_zone.side)
        return TacticalAction("move", target_zone=target_zone, comment="подключается к атаке")


class CentralDefender(TacticalRole):
    def __init__(self):
        super().__init__(
            name="Central Defender",
            suitable_positions=[Position.CENTER_BACK],
            key_attributes=[Tackling, Strength, Aerial, Positioning, Decisions]
        )

    def behave(self, player, zone_analyzer, current_zone) -> TacticalAction:
        if current_zone.zone_type == ZoneType.DEFENSE:
            return TacticalAction("tackle", comment="прессингует нападающего")
        target_zone = zone_analyzer.get_zone_by_type(ZoneType.DEFENSE, current_zone.side)
        return TacticalAction("move", target_zone=target_zone, comment="возвращается на позицию в обороне")


class BallWinningMidfielder(TacticalRole):
    def __init__(self):
        super().__init__(
            name="Ball Winning Midfielder",
            suitable_positions=[Position.CENTRAL_MIDFIELDER, Position.DEFENSIVE_MIDFIELDER],
            key_attributes=[Tackling, Aggression, Stamina, Decisions, Teamwork]
        )

    def behave(self, player, zone_analyzer, current_zone) -> TacticalAction:
        if current_zone.zone_type in [ZoneType.CENTER, ZoneType.AFTER_DEFENSE]:
            return TacticalAction("tackle", comment="агрессивно вступает в отбор")
        target_zone = zone_analyzer.get_zone_by_type(ZoneType.CENTER, current_zone.side)
        return TacticalAction("move", target_zone=target_zone, comment="перемещается ближе к мячу")


class AdvancedPlaymaker(TacticalRole):
    def __init__(self):
        super().__init__(
            name="Advanced Playmaker",
            suitable_positions=[Position.CENTRAL_MIDFIELDER, Position.ATTACKING_MIDFIELDER],
            key_attributes=[Passing, Creativity, Decisions, Technique]
        )

    def behave(self, player, zone_analyzer, current_zone) -> TacticalAction:
        if current_zone.zone_type == ZoneType.PRE_ATTACK:
            return TacticalAction("pass", comment="разыгрывает комбинацию")
        target_zone = zone_analyzer.get_zone_by_type(ZoneType.PRE_ATTACK, current_zone.side)
        return TacticalAction("move", target_zone=target_zone, comment="ищет пространство между линиями")


class Winger(TacticalRole):
    def __init__(self):
        super().__init__(
            name="Winger",
            suitable_positions=[Position.RIGHT_WINGER, Position.LEFT_WINGER],
            key_attributes=[Dribbling, Crossing, Pace, Technique, Movement]
        )

    def behave(self, player, zone_analyzer, current_zone) -> TacticalAction:
        if current_zone.zone_type == ZoneType.ATTACK:
            return TacticalAction("dribble", comment="на скорости обходит защитника")
        target_zone = zone_analyzer.get_zone_by_type(ZoneType.ATTACK, current_zone.side)
        return TacticalAction("move", target_zone=target_zone, comment="открывается по флангу")


class Poacher(TacticalRole):
    def __init__(self):
        super().__init__(
            name="Poacher",
            suitable_positions=[Position.CENTRE_FORWARD],
            key_attributes=[Shooting, Movement, Positioning, Pace, Technique]
        )

    def behave(self, player, zone_analyzer, current_zone) -> TacticalAction:
        if current_zone.zone_type == ZoneType.ATTACK:
            return TacticalAction("shoot", comment="готов нанести удар по воротам")
        target_zone = zone_analyzer.get_zone_by_type(ZoneType.ATTACK, current_zone.side)
        return TacticalAction("move", target_zone=target_zone, comment="ищет свободную зону для рывка")
