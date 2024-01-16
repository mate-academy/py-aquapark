from abc import ABC
from typing import Type


class IntegerRange:

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, obj: object, objtype: type) -> float:
        return getattr(obj, self.private_name)

    def __set__(self, obj: object, value: float) -> None:
        # validate value
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"{value} not in range "
                             f"[{self.min_amount} : {self.max_amount}]")
        setattr(obj, self.private_name, value)


class Visitor:
    def __init__(self, name: str, age: int,
                 weight: float, height: float) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: float, height: float) -> None:
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
    def __init__(self, name: str,
                 limitation_class: Type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
        except ValueError:  # catch if error_not_in_range from IntegerRange
            return False
        return True
