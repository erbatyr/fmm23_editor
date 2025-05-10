from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Type

from engine.field.zones import ZoneType
from engine.player_attributes import Attribute, GKReflexes, GKHandling, GKCommunication, GKAgility, Positioning, \
    Tackling, Crossing, Pace, Stamina, Strength, Aerial, Decisions, Aggression, Teamwork, Passing, Creativity, \
    Technique, Movement, Dribbling, Shooting
from engine.positions import Position
from engine.tactical_action import TacticalAction
from engine.utils.passing import find_best_pass_target


@dataclass
class TacticalRole(ABC):
    name: str
    suitable_positions: List[Position]
    key_attributes: List[Type[Attribute]]

    @abstractmethod
    def behave(self, player, context, zone_analyzer, current_zone) -> TacticalAction:
        pass


class Goalkeeper(TacticalRole):
    def __init__(self):
        super().__init__(
            name="Goalkeeper",
            suitable_positions=[Position.GOALKEEPER],
            key_attributes=[GKReflexes, GKHandling, GKCommunication, GKAgility, Positioning]
        )

    def behave(self, player, context, zone_analyzer, current_zone) -> TacticalAction:
        if context.ball.holder == player:
            target = find_best_pass_target(player, context)
            if target:
                return TacticalAction("pass", target_player=target, comment="начинает атаку пасом")
            return TacticalAction("hold", comment="ждёт вариантов для розыгрыша")
        return TacticalAction("move", target_zone=zone_analyzer.get_zone_by_type(ZoneType.DEFENSE, current_zone.side), comment="возвращается в ворота")


class FullBack(TacticalRole):
    def __init__(self):
        super().__init__(
            name="Full-Back",
            suitable_positions=[Position.RIGHT_BACK, Position.LEFT_BACK],
            key_attributes=[Tackling, Positioning, Crossing, Pace, Stamina]
        )

    def behave(self, player, context, zone_analyzer, current_zone) -> TacticalAction:
        if context.ball.holder == player:
            if current_zone.zone_type == ZoneType.PRE_ATTACK:
                return TacticalAction("cross", comment="навешивает в штрафную")
            target = find_best_pass_target(player, context)
            if target:
                return TacticalAction("pass", target_player=target, comment="пасует вдоль фланга")
            return TacticalAction("hold", comment="не решается на пас")
        else:
            return TacticalAction("move", target_zone=zone_analyzer.get_zone_by_type(ZoneType.AFTER_DEFENSE, current_zone.side), comment="держит фланг")


class CentralDefender(TacticalRole):
    def __init__(self):
        super().__init__(
            name="Central Defender",
            suitable_positions=[Position.CENTER_BACK],
            key_attributes=[Tackling, Strength, Aerial, Positioning, Decisions]
        )

    def behave(self, player, context, zone_analyzer, current_zone) -> TacticalAction:
        if context.ball.holder == player:
            target = find_best_pass_target(player, context)
            if target:
                return TacticalAction("pass", target_player=target, comment="пас на ближнего")
            return TacticalAction("hold", comment="не нашёл продолжения")
        elif current_zone.zone_type != ZoneType.DEFENSE:
            return TacticalAction("move", target_zone=zone_analyzer.get_zone_by_type(ZoneType.DEFENSE, current_zone.side), comment="возвращается в линию обороны")
        return TacticalAction("tackle", comment="прессингует нападающего")



class BallWinningMidfielder(TacticalRole):
    def __init__(self):
        super().__init__(
            name="Ball Winning Midfielder",
            suitable_positions=[Position.CENTRAL_MIDFIELDER, Position.DEFENSIVE_MIDFIELDER],
            key_attributes=[Tackling, Aggression, Stamina, Decisions, Teamwork]
        )

    def behave(self, player, context, zone_analyzer, current_zone) -> TacticalAction:
        if context.ball.holder == player:
            target = find_best_pass_target(player, context)
            if target:
                return TacticalAction("pass", target_player=target, comment="быстро отдаёт после отбора")
            return TacticalAction("hold", comment="ждёт партнёров")
        elif current_zone.zone_type in [ZoneType.CENTER, ZoneType.AFTER_DEFENSE]:
            return TacticalAction("tackle", comment="агрессивно вступает в отбор")
        return TacticalAction("move", target_zone=zone_analyzer.get_zone_by_type(ZoneType.CENTER, current_zone.side), comment="сжимает пространство")


class AdvancedPlaymaker(TacticalRole):
    def __init__(self):
        super().__init__(
            name="Advanced Playmaker",
            suitable_positions=[Position.CENTRAL_MIDFIELDER, Position.ATTACKING_MIDFIELDER],
            key_attributes=[Passing, Creativity, Decisions, Technique]
        )

    def behave(self, player, context, zone_analyzer, current_zone) -> TacticalAction:
        if context.ball.holder == player:
            target = find_best_pass_target(player, context)
            if target:
                return TacticalAction("pass", target_player=target, comment="отдаёт разрезающий пас")
            return TacticalAction("dribble", comment="берёт инициативу на себя")
        return TacticalAction("move", target_zone=zone_analyzer.get_zone_by_type(ZoneType.PRE_ATTACK, current_zone.side), comment="ищет пространство между линиями")


class Winger(TacticalRole):
    def __init__(self):
        super().__init__(
            name="Winger",
            suitable_positions=[Position.RIGHT_WINGER, Position.LEFT_WINGER],
            key_attributes=[Dribbling, Crossing, Pace, Technique, Movement]
        )

    def behave(self, player, context, zone_analyzer, current_zone) -> TacticalAction:
        if context.ball.holder == player:
            if current_zone.zone_type == ZoneType.ATTACK:
                return TacticalAction("dribble", comment="пытается обыграть фланг")
            target = find_best_pass_target(player, context)
            if target:
                return TacticalAction("pass", target_player=target, comment="передача вдоль фланга")
            return TacticalAction("hold", comment="замедляет темп")
        return TacticalAction("move", target_zone=zone_analyzer.get_zone_by_type(ZoneType.PRE_ATTACK, current_zone.side), comment="ждёт передачу")


class Poacher(TacticalRole):
    def __init__(self):
        super().__init__(
            name="Poacher",
            suitable_positions=[Position.CENTRE_FORWARD],
            key_attributes=[Shooting, Movement, Positioning, Pace, Technique]
        )

    def behave(self, player, context, zone_analyzer, current_zone) -> TacticalAction:
        if context.ball.holder == player:
            if current_zone.zone_type == ZoneType.ATTACK:
                return TacticalAction("shoot", comment="наносит удар по воротам")
            target = find_best_pass_target(player, context)
            if target:
                return TacticalAction("pass", target_player=target, comment="отпасовывает назад")
            return TacticalAction("hold", comment="не видит вариантов")
        return TacticalAction("move", target_zone=zone_analyzer.get_zone_by_type(ZoneType.ATTACK, current_zone.side), comment="ищет момент для рывка")

