from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, obj: Any, objtype: None = None) -> Any:
        return getattr(obj, self.private_name)

    def __set__(self, obj: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        if value < self.min_amount or value > self.max_amount:
            raise ValueError(f"Value must be between "
                             f"{self.min_amount} and {self.max_amount}")


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
            limitation_class: Any
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            # Try creating an instance of the limitation validator
            # with the visitor’s data
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except (TypeError, ValueError):
            # One or more values were outside allowed range or wrong type
            return False
