from abc import ABC
from typing import Any


class IntegerRange:
    """Restrict an integer attribute to an inclusive range."""

    def __init__(self, min_amount: int, max_amount: int) -> None:
        """Initialize the descriptor with minimum and maximum values."""
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        """Create the protected name used to store the attribute value."""
        self.protected_name = "_" + name

    def __get__(self, instance: object | None, owner: type) -> Any:
        """Return the descriptor or the stored attribute value."""
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: Any) -> None:
        """Validate and store an integer value on the instance."""
        if not isinstance(value, int):
            raise TypeError
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError
        setattr(instance, self.protected_name, value)


class Visitor:
    """Store a visitor's personal data."""

    def __init__(
        self,
        name: str,
        age: int,
        weight: int,
        height: int
    ) -> None:
        """Initialize a visitor with their personal parameters."""
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    """Store parameters used to validate access to a slide."""

    def __init__(
        self,
        age: int,
        weight: int,
        height: int
    ) -> None:
        """Initialize the validator with a visitor's parameters."""
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    """Validate access parameters for a children's slide."""

    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    """Validate access parameters for an adult slide."""

    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    """Represent a slide with its access limitations."""

    def __init__(
        self,
        name: str,
        limitation_class: type[SlideLimitationValidator]
    ) -> None:
        """Initialize a slide with a limitation validator class."""
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        """Return whether a visitor meets the slide limitations."""
        try:
            self.limitation_class(
                visitor.age,
                visitor.weight,
                visitor.height,
            )
        except (TypeError, ValueError):
            return False

        return True
