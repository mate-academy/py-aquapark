from abc import ABC, abstractmethod
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: Any, owner: Any) -> Any:
        return getattr(instance, "_" + self.name)

    def __set__(self, instance: Any, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            return
        setattr(instance, "_" + self.name, value)

    def __set_name__(self, owner: str, name: str) -> None:
        self.name = name


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

    @abstractmethod
    def can_access(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            age=IntegerRange(4, 14),
            weight=IntegerRange(20, 50),
            height=IntegerRange(80, 120),
        )

    def can_access(self, visitor: Visitor) -> bool:
        return all([
            self.age.min_amount <= visitor.age <= self.age.max_amount,
            self.height.min_amount <= visitor.height <= self.height.max_amount,
            self.weight.min_amount <= visitor.weight <= self.weight.max_amount,
        ])


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            age=IntegerRange(14, 60),
            weight=IntegerRange(50, 120),
            height=IntegerRange(120, 220),
        )

    def can_access(self, visitor: Visitor) -> bool:
        return all([
            self.age.min_amount <= visitor.age <= self.age.max_amount,
            self.height.min_amount <= visitor.height <= self.height.max_amount,
            self.weight.min_amount <= visitor.weight <= self.weight.max_amount
        ])


class Slide:
    def __init__(self, name: str, limitation_class: Any) -> None:
        self.name = name
        self.limitation = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation.can_access(visitor)
