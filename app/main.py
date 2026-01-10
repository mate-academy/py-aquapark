from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object | None, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __set__(self, instance: type, value: type) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be int")
        if value < self.min_amount or value > self.max_amount:
            raise ValueError("Value out of range")
        setattr(instance, self.protected_name, value)


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
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Any) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
        except Exception:
            return False
        return True
