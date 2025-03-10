from typing import List, Optional
from player import Player  # Импортируй свой Player класс
from positions import Position

class Team:
    def __init__(self, name: str, players: List[Player]):
        self.name = name
        self.players = players

    def get_goalkeeper(self) -> Optional[Player]:
        for player in self.players:
            if player.position == Position.GOALKEEPER:
                return player
        return None

    def get_players_by_position_group(self, group):
        return [p for p in self.players if p.position.group() == group]

    def __str__(self):
        return f"{self.name} ({len(self.players)} игроков)"
