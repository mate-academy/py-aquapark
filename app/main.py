from __future__ import annotations
from abc import ABC


class IntegerRange:
    def __init__(
            self,
            min_amount: int,
            max_amount: int
    ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(
            self,
            instance: int,
            owner: IntegerRange
    ) -> None:
        getattr(instance, self.name)

    def __set__(
            self,
            instance: int,
            value: int
    ) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.name, value)

    def __set_name__(
            self,
            owner: IntegerRange,
            name: str
    ) -> None:
        self.name = name


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age = IntegerRange(4, 14)
        height = IntegerRange(80, 120)
        weight = IntegerRange(20, 50)
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age = IntegerRange(14, 60)
        height = IntegerRange(120, 220)
        weight = IntegerRange(50, 120)
        super().__init__(age, weight, height)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return all(
            getattr(self.limitation_class, attr).min_amount
            <= getattr(visitor, attr)
            <= getattr(self.limitation_class, attr).max_amount
            for attr in ["age", "height", "weight"]
        )
