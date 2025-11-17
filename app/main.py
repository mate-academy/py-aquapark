from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount: int = min_amount
        self.max_amount: int = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.protected_name: str = "_" + name

    def __get__(self, instance: Any, owner: Any) -> int:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError("Value out of allowed range")
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name: str = name
        self.age: int = age
        self.weight: int = weight
        self.height: int = height


class SlideLimitationValidator(ABC):
    age: Any
    weight: Any
    height: Any

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
    def __init__(self, *, name: str, limitation_class: Any) -> None:
        self.name: str = name
        if isinstance(limitation_class, type):
            if limitation_class is ChildrenSlideLimitationValidator:
                self.limitation_validator = limitation_class(4, 20, 80)
            elif limitation_class is AdultSlideLimitationValidator:
                self.limitation_validator = limitation_class(14, 50, 120)
            else:
                self.limitation_validator = limitation_class(0, 0, 0)
        else:
            self.limitation_validator = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_validator.age = visitor.age
            self.limitation_validator.weight = visitor.weight
            self.limitation_validator.height = visitor.height
        except (TypeError, ValueError):
            return False
        return True
