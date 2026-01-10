from abc import ABC
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object, owner: Type) -> int:
        return instance.__dict__.get(self.name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"The value of {self.name} must be an integer")
        if value < self.min_amount or value > self.max_amount:
            raise ValueError(f"{self.name}"
                             f"must be between {self.min_amount}"
                             f" and {self.max_amount}")
        instance.__dict__[self.name] = value


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int,
                 height: int)\
            -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)

    def validate(self) -> bool:
        if not (4 <= self.age <= 14):
            raise ValueError("Children must be between 4 and 14 years old")
        if not (80 <= self.height <= 120):
            raise ValueError("Height for children"
                             " should be between 80 and 120 cm")
        if not (20 <= self.weight <= 50):
            raise ValueError("Weight for children"
                             " should be between 20 and 50 kg")
        return True


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)

    def validate(self) -> bool:
        if not (14 <= self.age <= 60):
            raise ValueError("Adults must be between 14 and 60 years old")
        if not (120 <= self.height <= 220):
            raise ValueError("Height for adults"
                             " should be between 120 and 220 cm")
        if not (50 <= self.weight <= 120):
            raise ValueError("Weight for adults"
                             " should be between 50 and 120 kg")
        return True


class Slide:
    def __init__(self, name: str,
                 limitation_class: Type[SlideLimitationValidator])\
            -> None:
        self.name = name
        self.limitation_class = limitation_class
        if not issubclass(limitation_class, SlideLimitationValidator):
            raise TypeError(f"{self.limitation_class}"
                            f" is not a subclass of SlideLimitationValidator")

    def can_access(self, visitor: Visitor) -> bool:
        limitation_validator = self.limitation_class(
            visitor.age, visitor.weight, visitor.height)
        try:
            return limitation_validator.validate()
        except ValueError as e:
            print(f"Access denied: {e}")
            return False
