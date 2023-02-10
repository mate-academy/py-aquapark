from __future__ import annotations

from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int = None, max_amount: int = None) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, other: SlideLimitationValidator, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self,
                other: SlideLimitationValidator,
                value: int or str) -> int or str:
        return getattr(other, self.protected_name)

    def __set__(self,
                other: SlideLimitationValidator,
                value: int or str) -> None:
        if type(value) != int:
            raise TypeError("Quantity should be integer.")
        if value < self.min_amount or value > self.max_amount:
            raise ValueError(
                f"Quantity should not be less than {self.min_amount}"
                f" and greater than {self.max_amount}.")
        setattr(other, self.protected_name, value)


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
    def __init__(self,
                 name: str,
                 limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, instance: Visitor) -> bool:
        try:
            self.limitation_class(instance.age, instance.weight,
                                  instance.height)
            return True
        except Exception:
            return False
