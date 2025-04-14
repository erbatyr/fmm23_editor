from typing import Dict

from engine.field.zones import FieldZone, ZoneType, Side
from engine.player import Player


class ZoneTracker:
    """
    Хранит и отслеживает текущую зону каждого игрока на поле.
    Позволяет получать и изменять зону, а также управлять передвижениями игроков.
    """
    def __init__(self):
        self._player_zones: Dict[Player, FieldZone] = {}

    def set_initial_zone(self, player: Player, zone: FieldZone):
        """Устанавливает стартовую зону для игрока (при старте матча)"""
        self._player_zones[player] = zone

    def move_player(self, player: Player, target_zone: FieldZone):
        """
        Перемещает игрока в новую зону. Позже сюда можно добавить механику скорости передвижения.
        """
        if player in self._player_zones:
            self._player_zones[player] = target_zone
        else:
            raise ValueError(f"Игрок {player.full_name} не имеет текущей зоны — используйте set_initial_zone()")

    def get_all_zones(self) -> Dict[Player, FieldZone]:
        """Возвращает словарь всех игроков и их текущих зон"""
        return self._player_zones

    def display_positions(self):
        """Печатает зоны всех игроков (для отладки)"""
        for player, zone in self._player_zones.items():
            print(f"{player.full_name} находится в зоне: {zone}")

    def update_player_zone(self, player: Player, new_zone: FieldZone):
        self._player_zones[player] = new_zone

    def get_player_zone(self, player: Player) -> FieldZone:
        return self._player_zones.get(player)

    @property
    def player_zones(self):
        return self._player_zones

# # Пример — установка зон игрокам
# zone_tracker = ZoneTracker()
# zone_tracker.set_initial_zone(player1, FieldZone(ZoneType.DEFENSE, Side.CENTER))
# zone_tracker.set_initial_zone(player2, FieldZone(ZoneType.PRE_ATTACK, Side.LEFT))
#
# # Получение зоны
# zone = zone_tracker.get_zone(player1)
# print(zone)
#
# # Перемещение игрока
# zone_tracker.move_player(player1, FieldZone(ZoneType.CENTER, Side.CENTER))
#
# # Показ всех позиций
# zone_tracker.display_positions()