from __future__ import annotations
from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: SlideLimitationValidator, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self,
                instance: SlideLimitationValidator,
                owner: SlideLimitationValidator) -> str | int:
        return getattr(instance, self.private_name)

    def __set__(self, instance: SlideLimitationValidator, value: str) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be Integer")
        if value < self.min_amount or value > self.max_amount:
            raise ValueError(f"Value should not be less than "
                             f"{self.min_amount} and greater than "
                             f"{self.max_amount}.")
        setattr(instance, self.private_name, value)


class Visitor:
    def __init__(self,
                 name: str,
                 age: int,
                 weight: int,
                 height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__()
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
    def __init__(self,
                 name: str,
                 limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        result = True
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
        except Exception:
            result = False
        return result
