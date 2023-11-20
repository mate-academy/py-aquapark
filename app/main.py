from __future__ import annotations

from typing import Type
from abc import ABC, abstractmethod


class IntegerRange:

    def __init__(self,
                 min_amount: int,
                 max_amount: int) -> None:

        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, obj: any, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, obj: any, owner: any) -> int:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: any, value: int) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(obj, self.protected_name, value)
        else:
            raise ValueError(f"Value out of range: {value}")


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
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def can_access(self) -> None:
        pass


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

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
            self.limitation_class(age=visitor.age,
                                  weight=visitor.weight,
                                  height=visitor.height)
        except ValueError:
            return False

        return True


#
#
Ad = AdultSlideLimitationValidator
s = Slide("ad", Ad)
v = Visitor("me", age = 5, height = 90, weight = 15)
print(s.can_access(v))
