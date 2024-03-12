from abc import ABC, abstractmethod
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: dict, owner: Any) -> Any:
        return instance.__dict__[self.name]

    def __set__(self, instance: dict, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError(f"{self.name} must be an integer.")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"{self.name} must be between {self.min_amount}"
                f" and {self.max_amount}."
            )
        instance.__dict__[self.name] = value

    def __set_name__(self, owner: Any, name: str) -> None:
        self.name = name


class Visitor:
    age = IntegerRange(0, 100)
    weight = IntegerRange(0, 200)
    height = IntegerRange(0, 300)

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age: int = None,
                 weight: int = None,
                 height: int = None
                 ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def can_access(self, visitor: Visitor) -> bool:
        age_range = 4 <= visitor.age <= 14
        height_range = 80 <= visitor.height <= 120
        weight_range = 20 <= visitor.weight <= 50
        return age_range and height_range and weight_range


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def can_access(self, visitor: Visitor) -> bool:
        age_range = 14 <= visitor.age <= 60
        height_range = 120 <= visitor.height <= 220
        weight_range = 50 <= visitor.weight <= 120
        return age_range and height_range and weight_range


class Slide:
    def __init__(self, name: str, limitation_class: Any) -> None:
        self.name = name
        self.limitation_validator = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_validator.can_access(visitor)
