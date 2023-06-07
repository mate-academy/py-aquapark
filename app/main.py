from abc import ABC
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object = None, owner: Type = None) -> None:
        if instance is None:
            return self
        return getattr(instance, self._protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("Value must be an integer.")
        if not self.min_amount <= value <= self.max_amount:
            raise (
                ValueError(f"Value must be between {self.min_amount} "
                           f"and {self.max_amount}.")
            )
        setattr(instance, self._protected_name, value)

    def __set_name__(self, owner: Type, name: str) -> None:
        self._protected_name = "_" + name


class Visitor:
    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide(SlideLimitationValidator):
    def __init__(
            self,
            name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                visitor.name,
                visitor.age, visitor.height,
                visitor.weight)
            return True
        except ValueError:
            return False
