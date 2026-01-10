from typing import Any
from abc import ABC


class IntegerRange:

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: Any, owner: type) -> Any:
        return getattr(instance, self.privat_name)

    def __set__(self, instance: Any, value: str) -> None:
        if not isinstance(value, int):
            raise TypeError
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError
        setattr(instance, self.privat_name, value)

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.privat_name = "_" + name


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

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)


class Slide:

    def __init__(self, name: str, limitation_class: Any) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, other: Visitor) -> bool:
        try:
            self.limitation_class(
                age=other.age,
                weight=other.weight,
                height=other.height)
            return True
        except (ValueError, TypeError):
            return False
