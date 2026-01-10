from abc import ABC
from typing import Callable


class IntegerRange:
    def __init__(self, min_amount: int,
                 max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: int, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: str, owner: int) -> None:
        getattr(instance, self.protected_name)

    def __set__(self, instance: str, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int,
                 weight: int, height: int) -> None:
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
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:

    def __init__(self, name: str, limitation_class: Callable) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            # Instantiate the limitation class
            validator = self.limitation_class(
                visitor.age,
                visitor.weight,
                visitor.height
            )
            # Validate each attribute
            validator.age = visitor.age
            validator.weight = visitor.weight
            validator.height = visitor.height
            return True
        except (TypeError, ValueError):
            return False
