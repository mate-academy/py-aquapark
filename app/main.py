from __future__ import annotations
from typing import Any

from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> int:
        return getattr(instance, self.name)

    def __set__(self, instance: Any, value: int) -> None:
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError
        setattr(instance, self.name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):

    def __init__(
            self,
            age: IntegerRange,
            weight: IntegerRange,
            height: IntegerRange
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14),
    weight = IntegerRange(20, 50),
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60),
    weight = IntegerRange(50, 120),
    height = IntegerRange(120, 220)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class.age = visitor.age
            self.limitation_class.weight = visitor.weight
            self.limitation_class.height = visitor.height
            return True
        except ValueError:
            return False
