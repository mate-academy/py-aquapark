from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, obj: Any) -> object:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: Any, value: int | float) -> None:
        if not isinstance(value, int | float):
            raise TypeError("when it comes to age, weight, height"
                            " - number expected :) ")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(f"for this piece of data value should be in the "
                             f"interval {self.min_amount} - {self.max_amount}")
        setattr(obj, self.protected_name, value)


class Visitor:
    def __init__(self,
                 name: str,
                 age: int | float,
                 weight: int | float,
                 height: int | float) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age: int | float,
                 weight: int | float,
                 height: int | float) -> None:
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
    def __init__(self,
                 name: str,
                 limitation_class: type(SlideLimitationValidator)) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, person: Visitor) -> bool:
        try:
            self.limitation_class(person.age, person.weight, person.height)
        except (TypeError, ValueError):
            return False
        return True
