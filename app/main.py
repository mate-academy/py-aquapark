from __future__ import annotations

from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount, self.max_amount = min_amount, max_amount

    def __set_name__(self, instance: IntegerRange, name: str) -> None:
        self.public_name, self.private_name = name, "_" + name

    def __get__(self, instance: IntegerRange, owner: str) -> int:
        return getattr(instance, self.private_name)

    def __set__(self, instance: IntegerRange, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")

        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"Value must be in range {self.min_amount}...{self.max_amount}"
            )

        setattr(instance, self.private_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name, self.age, self.weight, self.height = (
            name, age, weight, height
        )


class SlideLimitationValidator(ABC):
    @abstractmethod
    def __init__(self, age: int, weight: int, height: int) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age, self.weight, self.height = age, weight, height


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age, self.weight, self.height = age, weight, height


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool | None:
        try:
            self.limitation_class(
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height
            )
            return True
        except ValueError or TypeError:
            return False
