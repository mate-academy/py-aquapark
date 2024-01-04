from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, obj: Any, objtype: Any = None) -> int:
        return getattr(obj, self.private_name)

    def __set__(self, obj: Any, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"Should not be less than "
                             f"{self.min_amount} and greater than "
                             f"{self.max_amount}")
        setattr(obj, self.private_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: tuple[int, int],
                 weight: tuple[int, int],
                 height: tuple[int, int]) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age=(4, 14), weight=(20, 50), height=(80, 120))

    def validate(self, age: int, height: int, weight: int) -> bool:
        age_valid = self.age[0] <= age <= self.age[1]
        height_valid = self.height[0] <= height <= self.height[1]
        weight_valid = self.weight[0] <= weight <= self.weight[1]

        return age_valid and height_valid and weight_valid


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age=(14, 60), weight=(50, 120), height=(120, 220))

    def validate(self, age: int, height: int, weight: int) -> bool:
        age_valid = self.age[0] <= age <= self.age[1]
        height_valid = self.height[0] <= height <= self.height[1]
        weight_valid = self.weight[0] <= weight <= self.weight[1]

        return age_valid and height_valid and weight_valid


class Slide:
    def __init__(self, name: str,
                 limitation_class: type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_validator = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_validator.validate(
            visitor.age, visitor.height, visitor.weight)
