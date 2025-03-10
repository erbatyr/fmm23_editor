from enum import Enum


class Position(Enum):
    GOALKEEPER = "GK"
    RIGHT_BACK = "RB"
    CENTER_BACK = "CB"
    LEFT_BACK = "LB"
    RIGHT_WING_BACK = "RWB"
    LEFT_WING_BACK = "LWB"
    DEFENSIVE_MIDFIELDER = "CDM"
    RIGHT_MIDFIELDER = "RM"
    CENTRAL_MIDFIELDER = "CM"
    LEFT_MIDFIELDER = "LM"
    RIGHT_WINGER = "RW"
    ATTACKING_MIDFIELDER = "CAM"
    LEFT_WINGER = "LW"
    LEFT_INSIDE_FORWARD = "LIF"
    RIGHT_INSIDE_FORWARD = "RIF"
    CENTRE_FORWARD = "CF"

    def __str__(self):
        return self.value


    def group(self):
        if self in {Position.GOALKEEPER}:
            return "Goalkeeper"
        elif self in {Position.RIGHT_BACK, Position.LEFT_BACK, Position.CENTER_BACK, Position.RIGHT_WING_BACK,
                      Position.LEFT_WING_BACK}:
            return "Defender"
        elif self in {Position.DEFENSIVE_MIDFIELDER, Position.CENTRAL_MIDFIELDER, Position.RIGHT_MIDFIELDER,
                      Position.LEFT_MIDFIELDER, Position.ATTACKING_MIDFIELDER}:
            return "Midfielder"
        else:
            return "Forward"