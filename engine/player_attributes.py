from dataclasses import dataclass

@dataclass
class Attribute:
    value: int

    def modify(self, amount: int):
        """Изменяет значение характеристики (но не ниже 0 и не выше 100)"""
        self.value = max(0, min(20, self.value + amount))

    def __str__(self):
        return f"{self.__class__.__name__}: {self.value}"


@dataclass
class GKAgility(Attribute): pass
@dataclass
class GKCommunication(Attribute): pass
@dataclass
class GKHandling(Attribute): pass
@dataclass
class GKKicking(Attribute): pass
@dataclass
class GKReflexes(Attribute): pass

@dataclass
class Aerial(Attribute): pass
@dataclass
class Crossing(Attribute): pass
@dataclass
class Dribbling(Attribute): pass
@dataclass
class Passing(Attribute): pass
@dataclass
class Shooting(Attribute): pass
@dataclass
class Tackling(Attribute): pass
@dataclass
class Technique(Attribute): pass
@dataclass
class Aggression(Attribute): pass
@dataclass
class Creativity(Attribute): pass
@dataclass
class Decisions(Attribute): pass
@dataclass
class Leadership(Attribute): pass
@dataclass
class Movement(Attribute): pass
@dataclass
class Positioning(Attribute): pass
@dataclass
class Teamwork(Attribute): pass
@dataclass
class Pace(Attribute): pass
@dataclass
class Stamina(Attribute): pass
@dataclass
class Strength(Attribute): pass
