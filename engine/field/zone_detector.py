from engine.field.zones import FieldZone


class ZoneDetector:
    def __init__(self, field_length: int = 500, field_width: int = 300):
        self.field_length = field_length  # Вертикаль (глубина атаки)
        self.field_width = field_width    # Горизонталь (ширина поля)

    def detect_zone(self, x: int, y: int) -> FieldZone:
        row_height = self.field_length // 5
        col_width = self.field_width // 3

        # Глубина зоны (по Y)
        if y < row_height:
            row = "DEFENSE"
        elif y < row_height * 2:
            row = "AFTER_DEFENSE"
        elif y < row_height * 3:
            row = "CENTER"
        elif y < row_height * 4:
            row = "PRE_ATTACK"
        else:
            row = "ATTACK"

        # Ширина зоны (по X)
        if x < col_width:
            col = "LEFT"
        elif x < col_width * 2:
            col = "CENTER"
        else:
            col = "RIGHT"

        return FieldZone[f"{row}_{col}"]
