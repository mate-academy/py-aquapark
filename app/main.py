from abc import ABC, abstractmethod
from typing import Any, Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: Any, owner: Type) -> int:
        return instance.__dict__.get(self.name, 0)

    def __set__(self, instance: Any, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer.")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                "Value must be within the range: "
                f"{self.min_amount}-{self.max_amount}"
            )
        instance.__dict__[self.name] = value

    def __set_name__(self, owner: Type, name: str) -> None:
        self.name = name


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = int(age)
        self.weight = int(weight)
        self.height = int(height)


class SlideLimitationValidator(ABC):
    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        self.age = IntegerRange(4, 14)
        self.weight = IntegerRange(20, 50)
        self.height = IntegerRange(80, 120)

    def validate(self, visitor: Visitor) -> bool:
        is_age_valid = (
            self.age.min_amount <= visitor.age <= self.age.max_amount
        )
        is_weight_valid = (
            self.weight.min_amount <= visitor.weight <= self.weight.max_amount
        )
        is_height_valid = (
            self.height.min_amount <= visitor.height <= self.height.max_amount
        )

        return is_age_valid and is_weight_valid and is_height_valid


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        self.age = IntegerRange(14, 60)
        self.weight = IntegerRange(50, 120)
        self.height = IntegerRange(120, 220)

    def validate(self, visitor: Visitor) -> bool:
        is_age_valid = (
            self.age.min_amount <= visitor.age <= self.age.max_amount
        )
        is_weight_valid = (
            self.weight.min_amount <= visitor.weight <= self.weight.max_amount
        )
        is_height_valid = (
            self.height.min_amount <= visitor.height <= self.height.max_amount
        )

        return is_age_valid and is_weight_valid and is_height_valid


class Slide:
    def __init__(self, name: str, limitation_class: Type) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.validate(visitor)
