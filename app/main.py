from __future__ import annotations
from abc import ABC
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(
            self,
            owner: Type[ChildrenSlideLimitationValidator
                        | AdultSlideLimitationValidator],
            name: str) -> None:
        self.public_name = "_" + name

    def __get__(
            self,
            instance: (ChildrenSlideLimitationValidator
                       | AdultSlideLimitationValidator),
            owner: Type[ChildrenSlideLimitationValidator
                        | AdultSlideLimitationValidator],
    ) -> int:
        return getattr(instance, self.public_name)

    def __set__(
            self,
            instance: (ChildrenSlideLimitationValidator
                       | AdultSlideLimitationValidator),
            value: int
    ) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.public_name, value)
        else:
            setattr(instance, self.public_name, None)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
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
            limitation_class: Type[ChildrenSlideLimitationValidator
                                   | AdultSlideLimitationValidator],
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        limitation = self.limitation_class(
            age=visitor.age,
            height=visitor.height,
            weight=visitor.weight
        )
        if all(
                [limitation.age,
                 limitation.height,
                 limitation.weight]
        ):
            return True

        return False
