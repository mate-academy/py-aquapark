from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, obj: Any, objtype: Any = None) -> int:
        return getattr(obj, self.private_name)

    def __set__(self, obj: Any, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be of type int")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError("Invalid value")
        setattr(obj, self.private_name, value)


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

    def is_valid(self) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class Slide:
    def __init__(self, name: str,
                 limitation_class: SlideLimitationValidator) -> None:
        self.name: str = name
        self.limitation_class: SlideLimitationValidator = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        result = True
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
        except ValueError:
            result = False
        return result
