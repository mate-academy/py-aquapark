from abc import ABC
from typing import Optional


class IntegerRange:
    def __init__(
        self,
        min_amount: int,
        max_amount: int
    ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(
        self,
        instance: object,
        owner: object
    ) -> Optional[int | str]:
        return getattr(instance, self.protected_name)

    def __set__(
        self,
        instance: object,
        value: Optional[int | str]
    ) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_amount} and greater than "
                             f"{self.max_amount}.")
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.height = height
        self.weight = weight
        self.age = age
        self.name = name


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.weight = weight
        self.height = height
        self.age = age


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
        self,
        name: str,
        limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height
            )
            return True
        except (TypeError, ValueError):
            return False
