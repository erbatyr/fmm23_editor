from engine.ball import Ball
from engine.field.zone_analyzer import ZoneAnalyzer
from engine.field.zones import FieldZone, ZoneType, Side
from itertools import product

from engine.team import Team


class MatchContext:
    def __init__(self, team_a: Team, team_b: Team):
        self.team_a = team_a
        self.team_b = team_b
        self.ball = Ball()
        self.ball.holder = team_a.players[0]
        all_zones = [FieldZone(zt, s) for zt, s in product(ZoneType, Side)]
        self.zone_analyzer = ZoneAnalyzer(zones=all_zones, ball=self.ball)
