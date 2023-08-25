from __future__ import annotations
from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: Any) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance: SlideLimitationValidator, owner: Any) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: SlideLimitationValidator, value: Any) -> None:
        if value in range(self.min_amount, self.max_amount + 1):
            setattr(instance, self.protected_name, True)
        else:
            raise ValueError(
                f"{self.public_name} should not be less than "
                f"{self.min_amount} and greater than {self.max_amount}"
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
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(
            self, name: str, limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, instance: Visitor) -> bool:
        try:
            self.limitation_class(
                instance.age, instance.weight, instance.height
            )
            return True
        except ValueError:
            return False
