from __future__ import annotations
from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Visitor, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Visitor, owner: Visitor) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Visitor, value: int) -> None:
        setattr(instance, self.protected_name, value)


class Visitor:
    age = IntegerRange(4, 60)
    weight = IntegerRange(20, 120)
    height = IntegerRange(80, 220)

    def __init__(
            self,
            name: str,
            age: int,
            weight: int | float,
            height: int | float
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int,
            weight: int | float,
            height: int | float) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def validate(self) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def validate(self) -> bool:
        return (self.age in range(4, 15)
                and self.weight in range(20, 51)
                and self.height in range(80, 121))


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def validate(self) -> bool:
        return (self.age in range(14, 61)
                and self.weight in range(50, 121)
                and self.height in range(120, 221))


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class(
            visitor.age,
            visitor.weight,
            visitor.height).validate()
