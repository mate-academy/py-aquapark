from __future__ import annotations
from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: IntegerRange, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Visitor, owner: IntegerRange) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Visitor, value: IntegerRange) -> None:
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int | IntegerRange,
            weight: int | IntegerRange,
            height: int | IntegerRange
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def can_access(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age = IntegerRange(4, 14)
        height = IntegerRange(80, 120)
        weight = IntegerRange(20, 50)
        super().__init__(age, weight, height)

    def can_access(self, visitor: Visitor) -> bool:
        return (
            self.age.min_amount <= visitor.age <= self.age.max_amount
            and self.weight.min_amount <= visitor.weight
            <= self.weight.max_amount and self.height.min_amount
            <= visitor.height <= self.height.max_amount
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age = IntegerRange(14, 60)
        height = IntegerRange(120, 220)
        weight = IntegerRange(50, 120)
        super().__init__(age, weight, height)

    def can_access(self, visitor: Visitor) -> bool:
        return (
            self.age.min_amount <= visitor.age <= self.age.max_amount
            and self.weight.min_amount <= visitor.weight
            <= self.weight.max_amount and self.height.min_amount
            <= visitor.height <= self.height.max_amount
        )


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.can_access(visitor)
