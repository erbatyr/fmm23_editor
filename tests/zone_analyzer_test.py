from itertools import product

from engine.ball import Ball
from engine.field.zone_analysis import ZoneAnalyzer
from engine.field.zones import FieldZone, ZoneType, Side
from engine.player import Player
from engine.player_attributes import Pace
from engine.player_tactical_roles import Winger
from engine.positions import Position

# Создаём игрока
player = Player(
    position=Position.RIGHT_WINGER,
    first_name="Mo",
    last_name="Salah",
    attributes={Pace: Pace(18)},
    tactical_role=Winger()
)

# Создаём зоны
all_zones = [FieldZone(zt, s) for zt, s in product(ZoneType, Side)]

# Создаём мяч
ball = Ball()
ball.move_to_zone(FieldZone(ZoneType.ATTACK, Side.LEFT))

# Создаём анализатор
analyzer = ZoneAnalyzer(zones=all_zones, ball=ball)

# Тестируем
current_zone = FieldZone(ZoneType.CENTER, Side.RIGHT)
target_zone = analyzer.analyze(player, current_zone)
print(f"{player.full_name} в {current_zone} -> Цель: {target_zone}")