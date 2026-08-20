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

    def __set_name__(self, owner, name) -> None:
        self.protected_name = f"_{name}"

    def __set__(self, instance, value) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("value should be a number")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"value should be between {self.min_amount} "
                f"and {self.max_amount}")
        setattr(instance, self.protected_name, value)

    def __get__(self, instance, owner) -> None:
        return getattr(instance, self.protected_name)


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            weight: float | int,
            height: float | int,
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int,
            weight: float | int,
            height: float | int,
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
            self,
            limitation_class: Type[SlideLimitationValidator],
            name: str
    ) -> None:
        self.limitation_class = limitation_class
        self.name = name

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height,
            )
            return True
        except (TypeError, ValueError):
            return False