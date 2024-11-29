from abc import ABC
from typing import Callable


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Callable, name: str) -> None:
        self.protected_name = "_" + name

    def __set__(self, instance: Callable, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        if not (self.max_amount >= value >= self.min_amount):
            raise ValueError
        setattr(instance, self.protected_name, value)

    def __get__(self, instance: Callable, owner: Callable) -> int:
        return getattr(instance, self.protected_name)


class Visitor:
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
            height: int | float
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
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
        except (TypeError, ValueError):
            return False
        return True
