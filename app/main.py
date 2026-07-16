from abc import ABC
from typing import Any, Type


class IntegerRange:
    """Descriptor that validates if a value is an integer within a range."""

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.protected_name = ""

    def __set_name__(self, owner: Any, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: Any, owner: Any) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer.")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"Value must be between {self.min_amount} "
                f"and {self.max_amount}."
            )
        setattr(instance, self.protected_name, value)


class Visitor:
    """Class representing a visitor with personal parameters."""

    def __init__(
        self, name: str, age: int, weight: int, height: int
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    """Base validator class without strict range limitations."""

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    """Validator for children's slides."""

    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    """Validator for adult slides."""

    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    """Class representing a water slide with specific limitations."""

    def __init__(
        self, name: str, limitation_class: Type[SlideLimitationValidator]
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
