from abc import ABC
from typing import Type


class IntegerRange:
    def __init__(self,
                 min_amount: int,
                 max_amount: int)\
            -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.value = None

    def __set_name__(self, owner: Type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object, owner: Type) -> (int, None):
        return self.value

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"{self.name} must be an integer.")
        if value < self.min_amount or value > self.max_amount:
            raise ValueError
        self.value = value


class Visitor:
    def __init__(self,
                 name: str,
                 age: int,
                 weight: int,
                 height: int)\
            -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age: int,
                 weight: int,
                 height: int)\
            -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age: IntegerRange = IntegerRange(4, 14)
    height: IntegerRange = IntegerRange(80, 120)
    weight: IntegerRange = IntegerRange(20, 50)

    def __init__(self,
                 age: int,
                 weight: int,
                 height: int)\
            -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age: IntegerRange = IntegerRange(14, 60)
    height: IntegerRange = IntegerRange(120, 220)
    weight: IntegerRange = IntegerRange(50, 120)

    def __init__(self,
                 age: int,
                 weight: int,
                 height: int)\
            -> None:
        super().__init__(age, weight, height)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: Type[SlideLimitationValidator])\
            -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except (TypeError, ValueError):
            return False
