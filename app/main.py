from abc import ABC, abstractmethod
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Type[object], name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: object, owner: Type[object]) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"{self.protected_name} should be an integer.")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"{self.protected_name} "
                             f"should be between {self.min_amount} "
                             f"and {self.max_amount}.")
        setattr(instance, self.protected_name, value)


class Visitor:
    age = IntegerRange(0, 120)
    weight = IntegerRange(0, 200)
    height = IntegerRange(50, 250)

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: IntegerRange,
                 weight: IntegerRange,
                 height: IntegerRange) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(IntegerRange(4, 14),
                         IntegerRange(20, 50),
                         IntegerRange(80, 120))

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age.min_amount <= visitor.age
            <= self.age.max_amount
            and self.weight.min_amount <= visitor.weight
            <= self.weight.max_amount
            and self.height.min_amount <= visitor.height
            <= self.height.max_amount
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(IntegerRange(14, 60),
                         IntegerRange(50, 120),
                         IntegerRange(120, 220))

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age.min_amount <= visitor.age <= self.age.max_amount
            and self.weight.min_amount <= visitor.weight
            <= self.weight.max_amount
            and self.height.min_amount <= visitor.height
            <= self.height.max_amount
        )


class Slide:
    def __init__(self, name: str,
                 limitation_class: Type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.validate(visitor)
