from engine.field.zones import FieldZone
from player import Player

class Ball:
    def __init__(self, holder: Player = None, zone: FieldZone = None):
        self.holder = holder  # Кто владеет мячом
        self.zone = zone      # В какой зоне находится мяч (если свободен)

    def set_holder(self, player: Player):
        self.holder = player
        self.zone = None  # Когда мяч у игрока, его позиция — неактуальна

    def drop_ball(self, zone: FieldZone):
        self.zone = zone
        self.holder = None

    def move_to_zone(self, zone: FieldZone):
        self.zone = zone

    def __str__(self):
        if self.holder:
            return f"Ball controlled by {self.holder.full_name}"
        elif self.zone:
            return f"Ball is free in zone {self.zone}"
        return "Ball status unknown"
