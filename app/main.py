from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type


class IntegerRange:

    def __init__(self,
                 min_amount: int,
                 max_amount: int) -> None:

        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, obj: any, name: str) -> None:
        self.name = f"_{name}"

    def __get__(self, obj: any, owner: any) -> int:
        return getattr(obj, self.name)

    def __set__(self, obj: any, value: int) -> None:

        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError("Not in range")

        setattr(obj, self.name, value)


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

    def __init__(self,
                 age: int,
                 weight: int,
                 height: int) -> None:

        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def can_access(self) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14),
    weigh = IntegerRange(20, 50),
    height = IntegerRange(80, 120)

    # def __init__(self,
    #              age: int,
    #              weight: int,
    #              height: int) -> None:
    #     super().__init__(age, weight, height)

    def can_access(self) -> None:
        pass


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60),
    weigh = IntegerRange(50, 120),
    height = IntegerRange(120, 220)

    # def __init__(self,
    #              age: int,
    #              weight: int,
    #              height: int) -> None:
    #     super().__init__(age, weight, height)

    def can_access(self) -> None:
        pass


class Slide:

    def __init__(self,
                 name: str,
                 limitation_class: Type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:

        try:
            self.limitation_class(visitor.age,  visitor.weight, visitor.height)
        except ValueError:
            return False

        return True
