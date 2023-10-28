from abc import ABC, abstractmethod
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: int, owner: int) -> int:
        return instance.__dict__[self.name]

    def __set__(self, instance: int, value: int) -> int:
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError((f"{self.name} "
                              f"must be between {self.min_amount} "
                              f"and {self.max_amount}"))
        instance.__dict__[self.name] = value

    def __set_name__(self, owner: str, name: str) -> str:
        self.name = name


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        self.age: IntegerRange = IntegerRange(4, 14)
        self.height: IntegerRange = IntegerRange(80, 120)
        self.weight: IntegerRange = IntegerRange(20, 50)

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age.min_amount <= visitor.age <= self.age.max_amount
            and self.height.min_amount <= visitor.height
            <= self.height.max_amount
            and self.weight.min_amount <= visitor.weight
            <= self.weight.max_amount
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        self.age: IntegerRange = IntegerRange(14, 60)
        self.height: IntegerRange = IntegerRange(120, 220)
        self.weight: IntegerRange = IntegerRange(50, 120)

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age.min_amount <= visitor.age <= self.age.max_amount
            and self.height.min_amount <= visitor.height
            <= self.height.max_amount
            and self.weight.min_amount <= visitor.weight
            <= self.weight.max_amount
        )


class Slide:
    def __init__(self, name: str,
                 limitation_class: Type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class: SlideLimitationValidator = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.validate(visitor)
