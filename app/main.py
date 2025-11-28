from __future__ import annotations

from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        if not isinstance(min_amount, int) or not isinstance(max_amount, int):
            raise TypeError("bounds must be integers")
        if min_amount > max_amount:
            raise ValueError("min_amount > max_amount")
        self.min_amount: int = min_amount
        self.max_amount: int = max_amount
        self._attr_name: str | None = None

    def __set_name__(self, owner: type, name: str) -> None:
        self._attr_name = f"_{name}"

    def __get__(self, instance: object, owner: type) -> object | None:
        if instance is None:
            return self
        return getattr(instance, self._attr_name, None)

    def __set__(self, instance: object, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("value must be int")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError("out of range")
        setattr(instance, self._attr_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name: str = name
        self.age: int = age
        self.weight: int = weight
        self.height: int = height


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
        self,
        name: str,
        limitation_class: type[SlideLimitationValidator],
    ) -> None:
        if not isinstance(limitation_class, type) or not issubclass(
            limitation_class,
            SlideLimitationValidator,
        ):
            raise TypeError("invalid limitation_class")
        self.name: str = name
        self.limitation_class: (
            type[SlideLimitationValidator]
        ) = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                visitor.age,
                visitor.weight,
                visitor.height,
            )
            return True
        except Exception:
            return False
