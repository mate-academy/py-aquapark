from abc import ABC
from typing import Any


class IntegerRange:

    def __init__(
            self,
            min_amount: int,
            max_amount: int
    ) -> None:

        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, instance: object, owner: Any) -> float:
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: float) -> float | None:
        if self.min_amount <= value <= self.max_amount:
            return setattr(instance, self.private_name, value)
        raise ValueError(f"Value must be"
              f"{self.min_amount}...{self.max_amount}")


class Visitor:

    def __init__(
            self,
            name: str,
            age: int,
            weight: float,
            height: float) -> None:

        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):

    def __init__(
            self,
            name: str,
            age: int,
            weight: float,
            height: float) -> None:

        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(min_amount=4, max_amount=14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(min_amount=14, max_amount=60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:

    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:

        self.limitation_class = limitation_class
        self.name = name

    def can_access(self, visitor: Visitor) -> bool:
        try:
            instance = self.limitation_class(visitor.name,
                                             visitor.age,
                                             visitor.weight,
                                             visitor.height)
            return True if instance else False
        except ValueError:
            return False
