from typing import List

from engine.ball import Ball
from engine.player import Player
from engine.team import Team


class MatchContext:
    def __init__(self, team_a: Team, team_b: Team):
        self.team_a = team_a
        self.team_b = team_b
        self.all_players: List[Player] = team_a.players + team_b.players
        self.ball = Ball()

    def get_opposing_team(self, player: Player) -> Team:
        return self.team_b if player in self.team_a.players else self.team_a
