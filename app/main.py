from __future__ import annotations
from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object, owner: type) -> IntegerRange:
        return getattr(instance, self.protected)

    def __set__(self, instance: object, value: int) -> None:
        setattr(instance, self.protected, value)

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected = "_" + name


class Visitor:
    def __init__(self,
                 name: str,
                 age: int,
                 height: int,
                 weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age: IntegerRange,
                 height: IntegerRange,
                 weight: IntegerRange) -> None:
        self.age = age
        self.height = height
        self.weight = weight

    @abstractmethod
    def can_access(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            age=IntegerRange(4, 14),
            height=IntegerRange(80, 120),
            weight=IntegerRange(20, 50)
        )

    def can_access(self, visitor: Visitor) -> bool:
        age, height, weight = self.age, self.height, self.weight
        return all([age.min_amount <= visitor.age <= age.max_amount,
                    height.min_amount <= visitor.height <= height.max_amount,
                    weight.min_amount <= visitor.weight <= weight.max_amount])


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            age=IntegerRange(14, 60),
            height=IntegerRange(120, 220),
            weight=IntegerRange(50, 120)
        )

    def can_access(self, visitor: Visitor) -> bool:
        age, height, weight = self.age, self.height, self.weight
        return all([age.min_amount <= visitor.age <= age.max_amount,
                    height.min_amount <= visitor.height <= height.max_amount,
                    weight.min_amount <= visitor.weight <= weight.max_amount])


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.can_access(visitor=visitor)
