from abc import ABC
from typing import Any, Type


class IntegerRange:
    def __init__(
            self,
            min_amount: int,
            max_amount: int,
    ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> Any:
        return getattr(instance, self.protected_name, None)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int | float):
            raise TypeError(f"Parameter should be integer, got {type(value)} ")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"Value should be between {self.min_amount} "
                f"and {self.max_amount}"
            )
        setattr(instance, self.protected_name, value)


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int,
            weight: float,
            height: float
    ) -> None:
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


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            weight: float,
            height: float
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class Slide:
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
                visitor.age, visitor.weight, visitor.height
            )
        except ValueError:
            print(
                f"Guest is not suitable for the slider due to restrictions"
                f" (age: {visitor.age}, weight: {visitor.weight},"
                f" height: {visitor.height}).")
            return False
        return True
