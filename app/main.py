from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.name = f"_{name}"

    def __get__(self, instance: Any, owner: Any) -> Any:
        return getattr(instance, self.name)

    def __set__(self, instance: Any, value: int) -> None:
        if (not isinstance(self.min_amount, int)
                and isinstance(self.max_amount, int)):
            raise TypeError("Min and Max amount must be integers!")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(f"Value must be between {self.min_amount} and {self.max_amount}")  # NOQA E501


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
    height = IntegerRange(min_amount=80, max_amount=120)
    weight = IntegerRange(min_amount=20, max_amount=50)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(min_amount=14, max_amount=60)
    height = IntegerRange(min_amount=120, max_amount=220)
    weight = IntegerRange(min_amount=50, max_amount=120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class Slide:
    def __init__(self, name: str, limitation_class: SlideLimitationValidator) -> None:  # NOQA E501
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except (TypeError, ValueError):
            return False
