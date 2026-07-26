from __future__ import annotations
from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: None , owner: None = None) -> None:
        if instance is None:
            return self
        return instance.__dict__[self.public_name]

    def __set__(self, instance: None, value: int) -> None:
        if type(value) is not int:
            raise TypeError()
        if value not in range(self.min_amount, self.max_amount + 1):
            raise ValueError()
        instance.__dict__[self.public_name] = value

    def __set_name__(self, owner: None, name: str) -> None:
        self.public_name = name


class Visitor:

    def __init__(self,
                 name: str,
                 age: int,
                 weight: int | float,
                 height: float | int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age: int,
                 weight: int | float,
                 height: float | int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def __init__(self,
                 age: int,
                 weight: int | float,
                 height: float | int
                 ) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def __init__(self,
                 age: int,
                 weight: int | float,
                 height: float | int
                 ) -> None:
        super().__init__(age, weight, height)


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
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height)
        except (TypeError, ValueError):
            return False
        return True
