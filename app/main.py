from __future__ import annotations
from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.max_amount = max_amount
        self.min_amount = min_amount

    def __get__(self, instance: SlideLimitationValidator,
                owner: None) -> list[int]:
        return getattr(instance, self.protected)

    def __set_name__(self, owner: SlideLimitationValidator, name: str) -> None:
        self.protected = "_" + name

    def __set__(self, instance: SlideLimitationValidator, value: any) -> None:
        value = [num for num in range(self.min_amount, self.max_amount + 1)]
        setattr(instance, self.protected, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: list[int] = None, weight: list[int] = None,
                 height: list[int] = None) -> None:
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
    def __init__(self, name: str,
                 limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        result = True
        if visitor.age not in self.limitation_class.age:
            result = False
        if visitor.height not in self.limitation_class.height:
            result = False
        if visitor.weight not in self.limitation_class.weight:
            result = False

        return result
