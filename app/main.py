from __future__ import annotations
from abc import ABC
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self,
                     owner: Type[SlideLimitationValidator],
                     name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self,
                instance: SlideLimitationValidator,
                owner: Type[SlideLimitationValidator],) -> str:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: SlideLimitationValidator, value: int) -> None:
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(f"Sorry, but {self.protected_name} of visitor"
                             f" not satisfy slide limitations "
                             f"{self.min_amount} - {self.max_amount}")

        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self,
                 name: str,
                 age: int,
                 weight: int,
                 height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):

    def __init__(self, age: int, height: int, weight: int, ) -> None:
        self.age = age
        self.height = height
        self.weight = weight


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
            name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                visitor.age,
                visitor.height,
                visitor.weight,
            )
        except ValueError:
            return False

        return True
