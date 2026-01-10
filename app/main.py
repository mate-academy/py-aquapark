from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> Any:
        self.protected_name = f"_{name}"

    def __get__(self, instance: Any, owner: Any) -> str:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError(f"{self.protected_name}"
                            f" must be an integer.")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"{self.protected_name} must be between"
                f" {self.min_amount} and {self.max_amount}."
            )
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int,
                 weight: int | float, height: int | float) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            validator = self.limitation_class()
            validator.age = visitor.age
            validator.weight = visitor.weight
            validator.height = visitor.height
            return True
        except (TypeError, ValueError):
            return False
