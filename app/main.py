from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> Any:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Grade should be integer")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"Grade should not be less than {self.min_amount} and greater "
                f"than {self.max_amount}"
            )
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        self.age = IntegerRange(4, 14)
        self.height = IntegerRange(80, 120)
        self.weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        self.age = IntegerRange(14, 60)
        self.height = IntegerRange(120, 220)
        self.weight = IntegerRange(50, 120)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        if (
                (
                    self.limitation_class.age.min_amount <= visitor.age
                    <= self.limitation_class.age.max_amount
                )
                and (
                    self.limitation_class.weight.min_amount <= visitor.weight
                    <= self.limitation_class.weight.max_amount
                )
                and (
                    self.limitation_class.height.min_amount <= visitor.height
                    <= self.limitation_class.height.max_amount
                )
        ):
            return True
        return False
