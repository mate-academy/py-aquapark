from __future__ import annotations
from abc import ABC
from typing import Type


class IntegerRange:
    def __init__(
            self,
            min_amount: int,
            max_amount: int
    ) -> None:
        self.max_amount = max_amount
        self.min_amount = min_amount

    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_attr = "_" + name

    def __set__(self, instance: object, value: int) -> None:
        if not (self.max_amount >= value >= self.min_amount):
            raise ValueError(
                f""
                f"Quantity should not be less than {self.max_amount} "
                f"and greater than {self.min_amount}"
            )
        if not isinstance(value, int):
            raise TypeError("Value should be integer.")
        setattr(instance, self.protected_attr, value)

    def __get__(self, instance: object, owner: object) -> int:
        return getattr(instance, self.protected_attr)


class Visitor:
    def __init__(
            self,
            name: int,
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
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(
            self, name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                visitor.age,
                visitor.weight,
                visitor.height
            )
        except (ValueError, TypeError):
            return False
        return True
