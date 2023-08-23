from __future__ import annotations
from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: Any) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance: SlideLimitationValidator, owner: Any) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: SlideLimitationValidator, value: Any) -> None:
        if value in range(self.min_amount, self.max_amount + 1):
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
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(self, name: str, limitation_class: Any) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, instance: Visitor) -> bool:
        limits = self.limitation_class(
            instance.age, instance.weight, instance.height
        )
        if limits.age and limits.weight and limits.height:
            return True
        return False
