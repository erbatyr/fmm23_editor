import random
from typing import List

from engine.ball import Ball
from engine.field.goal_zones import GOAL_ZONES
from engine.field.zone_tracking import ZoneTracker
from engine.player_attributes import Shooting, Positioning, GKReflexes, GKHandling
from engine.positions import Position
from engine.tactical_action import TacticalAction
from player import Player

def simulate_turn(players: List[Player], zone_tracker: ZoneTracker, zone_analyzer, ball: Ball):
    print("\n=== Симуляция хода ===")

    for player in players:
        current_zone = zone_tracker.get_zone(player)
        action = player.tactical_role.behave(player, zone_analyzer, current_zone)

        print(f"{player.full_name} ({player.tactical_role.name}): {action.description} → {action.comment}")

        if action.description == "move" and action.target_zone:
            zone_tracker.move_player(player, action.target_zone)
            print(f" → Перемещается в зону: {action.target_zone}")

        elif action.description == "pass":
            if ball.holder == player:
                if action.target_player:
                    ball.set_holder(action.target_player)
                    print(f" → Пас на {action.target_player.full_name}")
                elif action.target_zone:
                    ball.drop_ball(action.target_zone)
                    print(f" → Пас в свободную зону: {action.target_zone}")
            else:
                print(" ⚠️ Пас невозможен — у игрока нет мяча")

        elif action.description == "shoot":
            if ball.holder == player:
                print(f" ⚽️ {player.full_name} бьёт по воротам!")
                # Найдём вратаря соперника
                opposing_goalkeeper = None
                for p in all_players:
                    if p.position == Position.GOALKEEPER:
                        opposing_goalkeeper = p
                        break
                if opposing_goalkeeper:
                    if is_goal(player, action, opposing_goalkeeper):
                        print(f" 🥅 ГОООЛ!!! {player.full_name} забивает — вратарь {opposing_goalkeeper.full_name}"
                              f" не спас!")
                        ball.drop_ball(GOAL_ZONES["CENTER"])
                    else:
                        print(f" 🧤 СЕЙВ! {opposing_goalkeeper.full_name} спасает ворота от удара {player.full_name}")
                        ball.set_holder(opposing_goalkeeper)
                else:
                    print(" ⚠️ Нет вратаря! Удар автоматически считается голом.")
                    ball.drop_ball(GOAL_ZONES["CENTER"])
            else:
                print(" ⚠️ Удар невозможен — у игрока нет мяча")

        elif action.description == "tackle":
            if ball.holder and zone_tracker.get_zone(ball.holder) == current_zone:
                print(f" 💥 Отбор у {ball.holder.full_name}")
                ball.set_holder(player)

        elif action.description == "hold":
            if ball.holder != player:
                ball.set_holder(player)
                print(f" ⚽ {player.full_name} берет мяч под контроль")

    print(f"\nТекущее состояние мяча: {ball}")
    print("=== Конец хода ===\n")


def goalkeeper_save_chance(goalkeeper: Player) -> int:
    reflexes = goalkeeper.get_attribute(GKReflexes)
    handling = goalkeeper.get_attribute(GKHandling)
    positioning = goalkeeper.get_attribute(Positioning)
    return reflexes + handling + positioning + random.randint(0, 10)


def is_goal(player: Player, action: TacticalAction, goalkeeper: Player) -> bool:
    shooting_score = player.get_attribute(Shooting) + player.get_attribute(Positioning) + random.randint(0, 10)
    save_score = goalkeeper_save_chance(goalkeeper)
    return shooting_score > save_score

