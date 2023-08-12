from __future__ import annotations
from abc import ABC, abstractmethod


from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.name = None

    def __get__(self, instance: Visitor, owner: type) -> str:
        return instance.__dict__[self.name]

    def __set__(self, instance: Visitor, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"Value must be between {self.min_amount} "
                f"and {self.max_amount}"
            )
        instance.__dict__[self.name] = value

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
        self,
        age_range: tuple[int, int],
        weight_range: tuple[int, int],
        height_range: tuple[int, int],
    ) -> None:
        self.age_range = age_range
        self.weight_range = weight_range
        self.height_range = height_range

    @abstractmethod
    def validate(self, visitor: Visitor) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            age_range=(4, 14), weight_range=(20, 50), height_range=(80, 120)
        )

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age_range[0] <= visitor.age <= self.age_range[1]
            and self.weight_range[0] <= visitor.weight <= self.weight_range[1]
            and self.height_range[0] <= visitor.height <= self.height_range[1]
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            age_range=(14, 60), weight_range=(50, 120), height_range=(120, 220)
        )

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age_range[0] <= visitor.age <= self.age_range[1]
            and self.weight_range[0] <= visitor.weight <= self.weight_range[1]
            and self.height_range[0] <= visitor.height <= self.height_range[1]
        )


class Slide:
    def __init__(
        self, name: int, limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.validate(visitor)
