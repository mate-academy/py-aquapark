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
            name: str
    ) -> None:
        self.private_name = "_" + name

    def __get__(self,
                instance: Type[ChildrenSlideLimitationValidator
                               | AdultSlideLimitationValidator],
                owner: (ChildrenSlideLimitationValidator
                        | AdultSlideLimitationValidator) = None) -> int:
        return getattr(instance, self.private_name)

    def __set__(self,
                instance: Type[ChildrenSlideLimitationValidator
                               | AdultSlideLimitationValidator],
                value: int) -> None:
        if not self.min_amount <= value <= self.max_amount:
            setattr(instance, self.private_name, 0)
            return
        setattr(instance, self.private_name, value)


class Visitor:
    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, height: int, weight: int) -> None:
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
            limitation_class: Type[ChildrenSlideLimitationValidator
                                   | AdultSlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        validate = self.limitation_class(
            age=visitor.age, height=visitor.height, weight=visitor.weight
        )
        if all((validate.age, validate.height, validate.weight)):
            return True
        return False
