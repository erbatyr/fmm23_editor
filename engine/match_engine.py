from random import random

from engine.field.zone_tracking import ZoneTracker
from engine.field.zones import FieldZone
from engine.match_context import MatchContext
from engine.player_attributes import Shooting, GKReflexes, Tackling, Strength
from engine.tactical_action import TacticalAction


class MatchEngine:
    def __init__(self, context: MatchContext, zone_tracker: ZoneTracker):
        self.context = context
        self.zone_tracker = zone_tracker
        self.tick_count = 0
        self.score = {
            self.context.team_a.name: 0,
            self.context.team_b.name: 0
        }

    def run_match(self, ticks=10):
        for _ in range(ticks):
            self.tick()
        print("\n🎯 Match finished!")
        print(f"Score: {self.score}")

    def tick(self):
        """Один игровой шаг/момент (tick)"""
        self.tick_count += 1
        print(f"\n--- TICK {self.tick_count} ---")

        player_with_ball = self.context.ball.holder
        current_zone = self.zone_tracker.get_player_zone(player_with_ball)

        action = player_with_ball.tactical_role.behave(
            player=player_with_ball,
            context=self.context,
            zone_analyzer=self.context.zone_analyzer,
            current_zone=current_zone
        )

        print(f"{player_with_ball.full_name} performs action: {action}")

        self._process_action(player_with_ball, action)

    def _process_action(self, player, action: TacticalAction):
        if action.action_type == "move":
            new_zone = self._resolve_zone_move(player, action)
            self.zone_tracker.update_player_zone(player, new_zone)
            print(f"{player.full_name} moves to {new_zone}")

        elif action.action_type == "pass":
            self._process_pass(player)

        elif action.action_type == "shoot":
            self._process_shot(player)

        elif action.action_type == "tackle":
            self._process_tackle(player)

        elif action.action_type == "cross":
            self._process_cross(player)

        elif action.action_type == "hold":
            print(f"{player.full_name} holds the ball and waits.")

    def _resolve_zone_move(self, player, action: TacticalAction):
        if isinstance(action.target_zone, FieldZone):
            return action.target_zone
        else:
            return self.zone_tracker.get_player_zone(player)

    def _process_pass(self, player):
        teammates = [p for p in self.context.all_players if p != player]
        target = teammates[0]
        self.context.ball.holder = target
        print(f"{player.full_name} passes to {target.full_name}")

    def _process_shot(self, player):
        target_goalkeeper = self.context.get_opposing_team(player).get_goalkeeper()
        striker_value = player.get_attribute(Shooting)
        gk_reflex = target_goalkeeper.get_attribute(GKReflexes)
        save_chance = gk_reflex / (striker_value + gk_reflex + 1e-5)

        if random() > save_chance:
            print(f"⚽️ GOAL by {player.full_name}!")
            self.score[self.context.get_team(player).name] += 1
        else:
            print(f"🧤 SAVE by {target_goalkeeper.full_name}!")
            self.context.ball.holder = target_goalkeeper

    def _process_tackle(self, player):
        current_owner = self.context.ball.holder
        tackle_value = player.get_attribute(Tackling)
        strength = current_owner.get_attribute(Strength)
        win_chance = tackle_value / (tackle_value + strength + 1e-5)

        if random() < win_chance:
            print(f"{player.full_name} wins the ball!")
            self.context.ball.holder = player
        else:
            print(f"{player.full_name} failed to tackle.")

    def _process_cross(self, player):
        teammates = [p for p in self.context.all_players if p != player]
        target = teammates[0]
        self.context.ball.holder = target
        print(f"{player.full_name} sends a cross to {target.full_name}")
