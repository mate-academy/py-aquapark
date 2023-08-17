from __future__ import annotations
from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance: SlideLimitationValidator, owner: type) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: SlideLimitationValidator, value: int) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.protected_name, value)
        else:
            raise ValueError


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = IntegerRange(age.min_amount, age.max_amount)
        self.weight = IntegerRange(weight.min_amount, weight.max_amount)
        self.height = IntegerRange(height.min_amount, height.max_amount)


class ChildrenSlideLimitationValidator:
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class AdultSlideLimitationValidator:
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class Slide:
    def __init__(
        self, name: str, limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.height, visitor.weight)
            return True
        except ValueError:
            return False
