from engine.field.zones import FieldZone
from engine.player import Player


class ZoneAnalyzer:
    def analyze(self, player: Player, current_zone: FieldZone):
        # Простейшая логика: вернуть ближайшую атакующую/защитную зону
        return current_zone