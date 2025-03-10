from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Ball:
    position: tuple[int, int]  # x, y координаты на поле
    owner: Optional["Player"]  # игрок, владеющий мячом (или None, если мяч свободен)


@dataclass
class PlayerPositionState:
    player: "Player"
    position: tuple[int, int]  # x, y координаты игрока


class GameContext:
    def __init__(
        self,
        ball: Ball,
        own_team: List[PlayerPositionState],
        opponent_team: List[PlayerPositionState],
        field_size: tuple[int, int] = (100, 60)  # поле 100x60 по умолчанию
    ):
        self.ball = ball
        self.own_team = own_team
        self.opponent_team = opponent_team
        self.field_width, self.field_height = field_size

    # Методы, используемые ролями
    
    def ball_near_player(self, player: "Player", distance: float = 5.0) -> bool:
        pos = self.get_player_position(player)
        return self._distance(pos, self.ball.position) <= distance

    def is_in_goal_area(self, player: "Player") -> bool:
        pos = self.get_player_position(player)
        # Простейшая проверка — игрок в штрафной площади
        return pos[0] >= self.field_width - 10  # допустим, 10 метров — штрафная

    def get_player_position(self, player: "Player") -> tuple[int, int]:
        for p in self.own_team + self.opponent_team:
            if p.player == player:
                return p.position
        return (0, 0)  # если игрок не найден (не должно случиться)

    def opponent_nearby(self, player: "Player", radius: float = 5.0) -> bool:
        my_pos = self.get_player_position(player)
        for opponent in self.opponent_team:
            if self._distance(my_pos, opponent.position) <= radius:
                return True
        return False

    def teammate_nearby(self, player: "Player", radius: float = 5.0) -> bool:
        my_pos = self.get_player_position(player)
        for teammate in self.own_team:
            if teammate.player != player and self._distance(my_pos, teammate.position) <= radius:
                return True
        return False

    def _distance(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> float:
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
