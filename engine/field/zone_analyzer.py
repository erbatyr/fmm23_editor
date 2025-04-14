from typing import List, Optional
from engine.field.zones import FieldZone, ZoneType, Side
from engine.player import Player
from engine.ball import Ball

class ZoneAnalyzer:
    def __init__(self, zones: List[FieldZone], ball: Optional[Ball] = None):
        """
        Инициализация анализатора зон.
        :param zones: Список всех зон на поле.
        :param ball: Мяч, чтобы учитывать его позицию (опционально).
        """
        self.zones = zones
        self.ball = ball

    def get_zone_by_type(self, zone_type: ZoneType, side: Side) -> Optional[FieldZone]:
        """
        Находит зону по типу и стороне.
        :param zone_type: Тип зоны (например, ZoneType.ATTACK).
        :param side: Сторона зоны (например, Side.RIGHT).
        :return: FieldZone или None, если зона не найдена.
        """
        for zone in self.zones:
            if zone.zone_type == zone_type and zone.side == side:
                return zone
        return None

    def analyze(self, player: Player, current_zone: FieldZone) -> FieldZone:
        """
        Анализирует ситуацию и возвращает целевую зону для игрока.
        :param player: Игрок, для которого выбирается зона.
        :param current_zone: Текущая зона игрока.
        :return: Целевая FieldZone.
        """
        role_name = player.tactical_role.name

        # Логика для разных ролей
        if role_name == "Goalkeeper":
            # Вратарь всегда стремится к зоне защиты
            return self.get_zone_by_type(ZoneType.DEFENSE, current_zone.side) or current_zone
        elif role_name == "Central Defender":
            # Защитник возвращается в оборону или остаётся там
            return self.get_zone_by_type(ZoneType.DEFENSE, current_zone.side) or current_zone
        elif role_name == "Full-Back":
            # Фулл-бэк идёт в атаку, если мяч в атакующей зоне, иначе в оборону
            if self.ball and self.ball.zone and self.ball.zone.zone_type in [ZoneType.ATTACK, ZoneType.PRE_ATTACK]:
                return self.get_zone_by_type(ZoneType.PRE_ATTACK, current_zone.side) or current_zone
            return self.get_zone_by_type(ZoneType.AFTER_DEFENSE, current_zone.side) or current_zone
        elif role_name == "Ball Winning Midfielder":
            # Полузащитник стремится к центру или к мячу
            if self.ball and self.ball.zone:
                return self.ball.zone
            return self.get_zone_by_type(ZoneType.CENTER, current_zone.side) or current_zone
        elif role_name == "Advanced Playmaker":
            # Плеймейкер ищет пространство в зоне перед атакой
            return self.get_zone_by_type(ZoneType.PRE_ATTACK, current_zone.side) or current_zone
        elif role_name == "Winger":
            # Вингер бежит в атаку по флангу
            return self.get_zone_by_type(ZoneType.ATTACK, current_zone.side) or current_zone
        elif role_name == "Poacher":
            # Форвард ищет зону атаки
            return self.get_zone_by_type(ZoneType.ATTACK, current_zone.side) or current_zone

        # По умолчанию возвращаем текущую зону
        return current_zone

    def get_nearest_zone(self, current_zone: FieldZone, target_type: ZoneType) -> Optional[FieldZone]:
        """
        Находит ближайшую зону заданного типа (для будущих механик).
        :param current_zone: Текущая зона.
        :param target_type: Желаемый тип зоны.
        :return: Ближайшая FieldZone или None.
        """
        # Простая реализация: ищем первую подходящую зону
        for zone in self.zones:
            if zone.zone_type == target_type:
                return zone
        return None