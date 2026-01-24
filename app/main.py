from __future__ import annotations

from abc import ABC


class IntegerRange:
    def __init__(
        self,
        min_amount: int,
        max_amount: int,
    ) -> None:
        self.min_amount, self.max_amount = min_amount, max_amount

    def __get__(
        self,
        instance: object,
        owner: type,
    ) -> int | IntegerRange:
        return (
            self
            if instance is None
            else getattr(instance, self.protected_name)
        )

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError()
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError()
        setattr(instance, self.protected_name, value)

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name


class Visitor:
    def __init__(
        self,
        name: str,
        age: int,
        weight: int,
        height: int,
    ) -> None:
        self.name, self.age, self.weight, self.height = (
            name,
            age,
            weight,
            height,
        )


class SlideLimitationValidator(ABC):
    def __init__(
        self,
        age: int,
        weight: int,
        height: int,
    ) -> None:
        self.age, self.weight, self.height = age, weight, height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age, height, weight = (
        IntegerRange(4, 14),
        IntegerRange(80, 120),
        IntegerRange(20, 50),
    )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age, height, weight = (
        IntegerRange(14, 60),
        IntegerRange(120, 220),
        IntegerRange(50, 120),
    )


class Slide:
    def __init__(
        self,
        name: str,
        limitation_class: type,
    ) -> None:
        self.name, self.limitation_class = name, limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                visitor.age,
                visitor.weight,
                visitor.height,
            )
            return True
        except (ValueError, TypeError):
            return False
