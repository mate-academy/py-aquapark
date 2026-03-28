from __future__ import annotations

from abc import ABC
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self._min_amount = min_amount
        self._max_and_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.protected_name = "_" + name

    def __get__(self, obj: object, objtype: type = None) -> int:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: object, value: int) -> None:
        if not (self._min_amount <= value <= self._max_and_amount):
            raise ValueError(f"Value for "
                             f"{self.protected_name} must be between "
                             f"{self._min_amount} and "
                             f"{self._max_and_amount}")
        setattr(obj, self.protected_name, value)


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


class ChildrenSlideLimitationValidator(SlideLimitationValidator, ABC):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator, ABC):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(
            self, name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
        except (TypeError, ValueError):
            return False
        return True
