from abc import ABC, abstractmethod
from typing import Union


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object, owner: type) -> Union:
        return instance.__dict__[self.name]

    def __set__(self, instance: object, value: int) -> None:
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"{self.name} must be in the range"
                f" {self.min_amount}-{self.max_amount}")
        instance.__dict__[self.name] = value


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: tuple, weight: tuple, height: tuple) -> None:
        self.age = IntegerRange(*age)
        self.weight = IntegerRange(*weight)
        self.height = IntegerRange(*height)

    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__((4, 14), (20, 50), (80, 120))

    def validate(self, visitor: Visitor) -> bool:
        return (self.age.min_amount <= visitor.age <= self.age.max_amount
                and self.weight.min_amount <= visitor.weight
                <= self.weight.max_amount
                and self.height.min_amount <= visitor.height
                <= self.height.max_amount
                )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__((14, 60), (50, 120), (120, 220))

    def validate(self, visitor: Visitor) -> bool:
        return (self.age.min_amount <= visitor.age <= self.age.max_amount
                and self.weight.min_amount <= visitor.weight
                <= self.weight.max_amount
                and self.height.min_amount <= visitor.height
                <= self.height.max_amount
                )


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_validator = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_validator.validate(visitor)
