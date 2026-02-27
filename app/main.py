from __future__ import annotations

from abc import ABC
from collections.abc import Callable


class MyErrors(Exception):
    """Here mine errors"""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(
        self, instance: SlideLimitationValidator, owner: type
    ) -> str | int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: SlideLimitationValidator, value: int) -> None:
        setattr(instance, self.protected_name, value)
        if not isinstance(value, int):
            raise MyErrors(f"{value} should be int")
        if value not in range(self.min_amount, self.max_amount + 1):
            raise MyErrors(
                f"{self.protected_name}"
                f" = {value} not in range between"
                f" {self.min_amount} and {self.max_amount}"
            )


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
    weight = IntegerRange(80, 120)
    height = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(120, 220)
    height = IntegerRange(50, 120)


class Slide:
    def __init__(
        self, name: str, limitation_class: Callable[int, int, int]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.height, visitor.weight)
            return True
        except MyErrors as e_info:
            print(e_info)
            return False
