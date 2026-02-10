from __future__ import annotations
from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, obj: object, value: int) -> None:
        self.private_name = "_" + value

    def __get__(self, instance: object, obj: object) -> int:
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: int) -> bool | int:
        if not (self.min_amount <= value <= self.max_amount):
            return setattr(instance, self.private_name, False)
        setattr(instance, self.private_name, value)


class Visitor:
    def __init__(
            self, name: str,
            age: int, weight: int,
            height: float
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    @abstractmethod
    def __init__(
            self, age: int,
            weight: int | float,
            height: int | float
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def __init__(
            self, age: int,
            weight: int | float,
            height: int | float
    ) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def __init__(
            self, age: int,
            weight: int | float,
            height: int | float
    ) -> None:
        super().__init__(age, weight, height)


class Slide:
    def __init__(
            self, name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        limit = self.limitation_class(
            visitor.age,
            visitor.weight,
            visitor.height
        )
        return all([limit._age, limit._weight, limit._height])
