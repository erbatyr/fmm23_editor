from engine.field.zones import FieldZone, ZoneType, Side


# Примитивное определение ворот
GOAL_ZONES = {
    "LEFT": FieldZone(zone_type=ZoneType.DEFENSE, side=Side.LEFT),
    "CENTER": FieldZone(zone_type=ZoneType.DEFENSE, side=Side.CENTER),
    "RIGHT": FieldZone(zone_type=ZoneType.DEFENSE, side=Side.RIGHT)
}
