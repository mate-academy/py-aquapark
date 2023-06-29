from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.visitor = "_" + name

    def __get__(self, instance: object, owner: type) -> object:
        return getattr(self.visitor, instance)

    def __set__(self, instance: object, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError(f"{value} is not integer")
        if value not in range(self.min_amount, self.max_amount + 1):
            raise ValueError(
                f"{value} not in range "
                f"{self.min_amount} - {self.max_amount}"
            )
        setattr(instance, self.visitor, value)


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
    age = IntegerRange(min_amount=4, max_amount=14)
    weight = IntegerRange(min_amount=20, max_amount=50)
    height = IntegerRange(min_amount=80, max_amount=120)


class AdultSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(min_amount=14, max_amount=60)
    weight = IntegerRange(min_amount=50, max_amount=120)
    height = IntegerRange(min_amount=120, max_amount=220)


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
                visitor.age,
                visitor.weight,
                visitor.height
            )
            return True
        except ValueError:
            return False
