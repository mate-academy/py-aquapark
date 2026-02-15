from __future__ import annotations
from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self._protected_name = "_" + name

    def __set__(self, instance: object, value: int) -> None | IntegerRange:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer.")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"Value must be between {self.min_amount} "
                             f"and {self.max_amount}.")
        if instance is None:
            return self
        return getattr(instance, self._protected_name, None)
        setattr(instance, self._protected_name, value)

    def __get__(self, instance: object, owner: type) -> int:
        return getattr(instance, self._protected_name, None)


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
    age: int = IntegerRange(4, 14)
    height: int = IntegerRange(80, 120)
    weight: int = IntegerRange(20, 50)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age: int = IntegerRange(14, 60)
    height: int = IntegerRange(120, 220)
    weight: int = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except Exception:
            return False
