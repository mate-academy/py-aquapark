from __future__ import annotations
from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(
        self,
        instance: SlideLimitationValidator,
        owner: type
    ) -> SlideLimitationValidator:
        return getattr(instance, self.protected_name)

    def __set__(
        self,
        instance: SlideLimitationValidator,
        value: int
    ) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be integer")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"Value must be in the range of "
                f"{self.min_amount} to {self.max_amount}"
            )
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(
        self,
        name: str,
        age: int,
        weight: int,
        height: int
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class Slide:
    def __init__(
        self,
        name: str,
        limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, person: Visitor) -> bool:
        try:
            slide = self.limitation_class
            slide(person.age, person.weight, person.height)
        except (TypeError, ValueError):
            return False
        return True
