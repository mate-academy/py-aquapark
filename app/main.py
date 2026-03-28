from __future__ import annotations
from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(
            self,
            owner: type[SlideLimitationValidator],
            name: str
    ) -> None:
        self.protected_name: str = "_" + name

    def __get__(self, obj: object, objtype: type | None = None) -> int:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        if value < self.min_amount or value > self.max_amount:
            raise ValueError
        setattr(obj, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name: str = name
        self.age: int = age
        self.weight: int = weight
        self.height: int = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age: int = age
        self.weight: int = weight
        self.height: int = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age: IntegerRange = IntegerRange(4, 14)
    weight: IntegerRange = IntegerRange(20, 50)
    height: IntegerRange = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age: IntegerRange = IntegerRange(14, 60)
    weight: IntegerRange = IntegerRange(50, 120)
    height: IntegerRange = IntegerRange(120, 220)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name: str = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except (TypeError, ValueError):
            return False
