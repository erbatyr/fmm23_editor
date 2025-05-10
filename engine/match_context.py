from itertools import product

from engine.ball import Ball
from engine.field.zone_analysis import ZoneAnalyzer
from engine.field.zone_tracking import ZoneTracker
from engine.field.zones import FieldZone, ZoneType, Side
from engine.team import Team


class MatchContext:
    def __init__(self, team_a: Team, team_b: Team):
        self.team_a = team_a
        self.team_b = team_b
        self.ball = Ball()
        self.ball.holder = team_a.players[0]  # первый игрок владеет мячом
        self.zone_tracker = ZoneTracker()

        all_zones = [FieldZone(zt, s) for zt, s in product(ZoneType, Side)]
        self.zone_analyzer = ZoneAnalyzer(
            zones=all_zones,
            match_context=self,
            zone_tracker=self.zone_tracker,
            ball=self.ball
        )

    def get_team(self, player):
        if player in self.team_a.players:
            return self.team_a
        elif player in self.team_b.players:
            return self.team_b
        else:
            raise ValueError("Player not found in either team.")

    def get_opposing_team(self, player):
        if player in self.team_a.players:
            return self.team_b
        elif player in self.team_b.players:
            return self.team_a
        else:
            raise ValueError("Player not found in either team.")

    @property
    def all_players(self):
        return self.team_a.players + self.team_b.players
