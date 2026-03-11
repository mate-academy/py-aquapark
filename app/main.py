from abc import ABC
from typing import Any, Type


class IntegerRange:
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.private_name: str | None = None

    def __set_name__(self, owner: type, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, instance: Any, owner: type) -> int:
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: Any, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be int")

        if not self.min_value <= value <= self.max_value:
            raise ValueError("Value out of range")

        setattr(instance, self.private_name, value)


class Visitor:
    def __init__(
        self,
        name: str,
        age: int,
        height: int,
        weight: int,
    ) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def __init__(
        self,
        age: int,
        height: int,
        weight: int,
    ) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(self, name: str, limitation_class: Type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                visitor.age,
                visitor.height,
                visitor.weight,
            )
            return True
        except (TypeError, ValueError):
            return False
