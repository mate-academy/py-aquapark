from __future__ import annotations
from typing import Any
from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        value = getattr(obj, self.private_name)
        return value

    def __set__(self, obj: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError
        setattr(obj, self.private_name, value)


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: float, weight: float, height: float) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: float, weight: float, height: float) -> None:
        self.age = age
        self.height = height
        self.weight = weight
        super().__init__(self.age, self.weight, self.height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: float, weight: float, height: float) -> None:
        self.age = age
        self.height = height
        self.weight = weight
        super().__init__(self.age, self.weight, self.height)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class:
            ChildrenSlideLimitationValidator | AdultSlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except (ValueError, TypeError):
            return False
