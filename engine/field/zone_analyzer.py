from collections import defaultdict
from typing import List, Dict

from engine.field.zones import FieldZone


class ZoneAnalyzer:
    def __init__(self, all_players: List['Player']):
        self.all_players = all_players
        self.zone_data = defaultdict(list)  # FieldZone -> List[Player]

        self._map_players_to_zones()

    def _map_players_to_zones(self):
        for player in self.all_players:
            if hasattr(player, "current_zone"):
                self.zone_data[player.current_zone].append(player)

    def player_density(self, zone: FieldZone) -> int:
        """Количество всех игроков в зоне"""
        return len(self.zone_data.get(zone, []))

    def team_density(self, zone: FieldZone, team: str) -> int:
        """Количество игроков одной команды в зоне"""
        return sum(1 for player in self.zone_data.get(zone, []) if player.team == team)

    def opponent_density(self, zone: FieldZone, team: str) -> int:
        """Количество игроков соперника в зоне"""
        return sum(1 for player in self.zone_data.get(zone, []) if player.team != team)

    def free_space_score(self, zone: FieldZone, max_ideal_players: int = 3) -> float:
        """Оценка свободного пространства: чем меньше игроков — тем выше"""
        density = self.player_density(zone)
        return max(0.0, max_ideal_players - density)

    def threat_level(self, zone: FieldZone, team: str) -> float:
        """Оценка угрозы в зоне: если много соперников — зона опасна"""
        opponents = self.opponent_density(zone, team)
        teammates = self.team_density(zone, team)
        return opponents - teammates  # Простая метрика (можно улучшать)

    def get_zone_report(self, zone: FieldZone, team: str) -> Dict[str, float]:
        return {
            "player_density": self.player_density(zone),
            "team_density": self.team_density(zone, team),
            "opponent_density": self.opponent_density(zone, team),
            "free_space_score": self.free_space_score(zone),
            "threat_level": self.threat_level(zone, team),
        }
