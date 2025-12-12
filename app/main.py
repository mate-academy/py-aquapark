from __future__ import annotations

from typing import Any, Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, instance: Any, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError(f"The '{self.public_name}' must be an integer.")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"The '{self.public_name}' must be between "
                f"{self.min_amount} and {self.max_amount} (inclusive)."
            )
        setattr(instance, self.private_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height

    def __repr__(self) -> str:
        return (
            f"Visitor(name='{self.name}', age={self.age}, "
            f"weight={self.weight}kg, height={self.height}cm)"
        )


class SlideLimitationValidator:
    age: IntegerRange
    weight: IntegerRange
    height: IntegerRange

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
        self,
        name: str,
        limitation_class: Type[SlideLimitationValidator],
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height,
            )
            return True
        except (TypeError, ValueError):
            return False

    def __repr__(self) -> str:
        return (
            f"Slide(name='{self.name}', "
            f"limitation_class={self.limitation_class.__name__})"
        )
