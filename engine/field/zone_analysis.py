from typing import List, Optional

from engine.ball import Ball
from engine.field.zone_tracking import ZoneTracker
from engine.field.zones import FieldZone, ZoneType, Side
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine.match_context import MatchContext
from engine.player import Player


class ZoneAnalyzer:
    def __init__(
        self,
        zones: List[FieldZone],
        match_context: "MatchContext",
        zone_tracker: ZoneTracker,
        ball: Optional[Ball] = None
    ):
        """
        Инициализация анализатора зон.
        :param zones: Список всех зон на поле.
        :param match_context: Контекст матча для доступа к командам.
        :param zone_tracker: Отслеживание зон игроков.
        :param ball: Мяч для учёта его позиции (опционально).
        """
        self.zones = zones
        self.match_context = match_context
        self.zone_tracker = zone_tracker
        self.ball = ball

    def get_zone_by_type(self, zone_type: ZoneType, side: Side) -> Optional[FieldZone]:
        """
        Находит зону по типу и стороне.
        """
        for zone in self.zones:
            if zone.zone_type == zone_type and zone.side == side:
                return zone
        return None

    def count_opponents_in_zone(self, player: Player, zone: FieldZone) -> int:
        """
        Подсчитывает количество соперников в заданной зоне.
        :param player: Игрок, для которого проверяем.
        :param zone: Зона для анализа.
        :return: Число соперников.
        """
        opponent_team = self.match_context.get_opposing_team(player)
        count = 0
        for opponent in opponent_team.players:
            opponent_zone = self.zone_tracker.get_player_zone(opponent)
            if opponent_zone == zone:
                count += 1
        return count

    def find_least_crowded_zone(self, player: Player, zone_type: ZoneType) -> Optional[FieldZone]:
        """
        Находит зону заданного типа с наименьшим количеством соперников.
        :param player: Игрок, для которого ищем зону.
        :param zone_type: Тип зоны (например, ZoneType.ATTACK).
        :return: Зона с минимумом соперников или None.
        """
        possible_zones = [
            zone for zone in self.zones if zone.zone_type == zone_type
        ]
        if not possible_zones:
            return None

        # Сортируем зоны по количеству соперников
        zone_counts = [
            (zone, self.count_opponents_in_zone(player, zone))
            for zone in possible_zones
        ]
        zone_counts.sort(key=lambda x: x[1])  # Сортировка по числу соперников
        return zone_counts[0][0] if zone_counts else None

    def analyze(self, player: Player, current_zone: FieldZone) -> FieldZone:
        """
        Анализирует ситуацию и возвращает целевую зону для игрока с учётом соперников.
        """
        role_name = player.tactical_role.name
        opponent_team = self.match_context.get_opposing_team(player)

        if role_name == "Goalkeeper":
            # Вратарь игнорирует соперников, остаётся в воротах
            return self.get_zone_by_type(ZoneType.DEFENSE, current_zone.side) or current_zone

        elif role_name == "Central Defender":
            # Защитник ищет нападающих в зоне Defense или After-Defense
            for opponent in opponent_team.players:
                opponent_zone = self.zone_tracker.get_player_zone(opponent)
                if opponent_zone and opponent_zone.zone_type in [ZoneType.DEFENSE, ZoneType.AFTER_DEFENSE]:
                    return opponent_zone  # Следовать за нападающим
            return self.get_zone_by_type(ZoneType.DEFENSE, current_zone.side) or current_zone

        elif role_name == "Full-Back":
            # Фулл-бэк идёт в атаку, если мяч в атаке и мало соперников
            if self.ball and self.ball.zone and self.ball.zone.zone_type in [ZoneType.ATTACK, ZoneType.PRE_ATTACK]:
                target_zone = self.get_zone_by_type(ZoneType.PRE_ATTACK, current_zone.side)
                if target_zone and self.count_opponents_in_zone(player, target_zone) < 2:
                    return target_zone
            return self.get_zone_by_type(ZoneType.AFTER_DEFENSE, current_zone.side) or current_zone

        elif role_name == "Ball Winning Midfielder":
            # Полузащитник бежит к мячу или в зону с минимумом соперников
            if self.ball and self.ball.zone:
                ball_zone = self.ball.zone
                if self.count_opponents_in_zone(player, ball_zone) <= 2:
                    return ball_zone
            return self.find_lowest_pressure_zone(player, ZoneType.CENTER) or current_zone

        elif role_name == "Advanced Playmaker":
            # Плеймейкер ищет свободную зону перед атакой
            target_zone = self.find_lowest_pressure_zone(player, ZoneType.PRE_ATTACK)
            return target_zone or self.get_zone_by_type(ZoneType.PRE_ATTACK, current_zone.side) or current_zone

        elif role_name == "Winger":
            # Вингер ищет свободную зону атаки
            target_zone = self.find_lowest_pressure_zone(player, ZoneType.ATTACK)
            return target_zone or self.get_zone_by_type(ZoneType.ATTACK, current_zone.side) or current_zone

        elif role_name == "Poacher":
            # Форвард ищет зону атаки с минимумом защитников
            target_zone = self.find_lowest_pressure_zone(player, ZoneType.ATTACK)
            return target_zone or self.get_zone_by_type(ZoneType.ATTACK, current_zone.side) or current_zone

        # По умолчанию — текущая зона
        return current_zone

    def count_teammates_in_zone(self, player: Player, zone: FieldZone) -> int:
        """
        Считает количество партнёров в заданной зоне.
        """
        team = self.match_context.get_team(player)
        return sum(
            1 for teammate in team.players
            if teammate != player and self.zone_tracker.get_player_zone(teammate) == zone
        )

    def calculate_pressure(self, player: Player, zone: FieldZone) -> int:
        """
        Давление в зоне: соперники - партнёры.
        Чем меньше значение, тем легче зоне.
        """
        opponents = self.count_opponents_in_zone(player, zone)
        teammates = self.count_teammates_in_zone(player, zone)
        return opponents - teammates

    def find_lowest_pressure_zone(self, player: Player, zone_type: ZoneType) -> Optional[FieldZone]:
        """
        Находит зону заданного типа с наименьшим давлением.
        """
        possible_zones = [z for z in self.zones if z.zone_type == zone_type]
        if not possible_zones:
            return None

        zone_pressures = [
            (zone, self.calculate_pressure(player, zone)) for zone in possible_zones
        ]
        zone_pressures.sort(key=lambda x: x[1])  # Чем ниже давление, тем лучше
        return zone_pressures[0][0]


    def zone_pressure(self, zone: FieldZone) -> float:
        team_a_count = sum(1 for p in self.match_context.team_a.players if self.zone_tracker.get_player_zone(p) == zone)
        team_b_count = sum(1 for p in self.match_context.team_b.players if self.zone_tracker.get_player_zone(p) == zone)

        total = team_a_count + team_b_count
        if total == 0:
            return 0.0

        # Давление — это плотность игроков в зоне
        return min(1.0, total / 6)  # например, 6 игроков = максимум давления
