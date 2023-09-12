from __future__ import annotations
from typing import Callable
from abc import ABC


class IntegerRange:
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner: SlideLimitationValidator, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Callable, objtype: None = None) -> bool:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Callable, value: int) -> None:
        if value in range(self.min_value, self.max_value + 1):
            setattr(instance, self.protected_name, True)
        else:
            setattr(instance, self.protected_name, False)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)


class Slide:
    def __init__(self, name: str, limitation_class: Callable) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        lim = self.limitation_class(
            visitor.age,
            visitor.weight,
            visitor.height
        )
        print(lim.age, lim.weight, lim.height)
        if lim.age and lim.height and lim.weight:
            return True
        return False
