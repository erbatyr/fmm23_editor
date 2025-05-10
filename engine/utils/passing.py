import random
from engine.player_attributes import Decisions, Creativity, Passing

def find_best_pass_target(player, context):
    # Awareness = по атрибутам
    awareness = (
        0.4 +
        0.02 * player.get_attribute(Decisions) +
        0.015 * player.get_attribute(Creativity) +
        0.015 * player.get_attribute(Passing)
    )

    if random.random() > awareness:
        return None  # игрок решил не отдавать пас

    own_team = context.get_team(player).players
    current_zone = context.zone_tracker.get_player_zone(player)
    best_score = -1
    best_target = None

    for teammate in own_team:
        if teammate == player:
            continue
        zone = context.zone_tracker.get_player_zone(teammate)
        if not zone:
            continue
        zone_priority = {
            "DEFENSE": 0,
            "AFTER_DEFENSE": 1,
            "CENTER": 2,
            "PRE_ATTACK": 3,
            "ATTACK": 4
        }

        score = 0
        score += zone_priority[zone.zone_type.name] * 10
        if zone.side == current_zone.side:
            score += 5
        pressure = context.zone_analyzer.zone_pressure(zone)
        score += int((1 - pressure) * 10)

        if score > best_score:
            best_score = score
            best_target = teammate

    return best_target
