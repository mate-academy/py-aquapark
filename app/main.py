from abc import ABC
from typing import Any


class IntegerRange:
    """
    Descriptor that validates an integer value falls within a given range.

    Implements the descriptor protocol (__set_name__, __get__, __set__)
    so instances can be used as class-level attributes that validate
    values on assignment.

    Raises TypeError if the value is not an integer, or ValueError if
    it falls outside [min_amount, max_amount].
    """

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: object | None, owner: type | None) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        if value < self.min_amount or value > self.max_amount:
            raise ValueError(
                f"Value must be between "
                f"{self.min_amount} and {self.max_amount}"
            )
        setattr(instance, self.protected_name, value)


class Visitor:
    """Represents an aquapark visitor with personal characteristics."""

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    """
    Abstract base class for slide access validators.

    Stores visitor parameters (age, weight, height) and validates them
    via IntegerRange descriptors defined in subclasses. Raises TypeError
    or ValueError on construction if any value is outside the allowed range.
    """

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    """
    Validates access for children:
    age 4–14, height 80–120 cm, weight 20–50 kg.
    """

    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    """
    Validates access for adults:
    age 14–60, height 120–220 cm, weight 50–120 kg.
    """

    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    """
    Represents an aquapark slide with a specific access policy.

    Uses a SlideLimitationValidator subclass to determine whether
    a given visitor meets the slide's age, weight, and height requirements.
    """

    def __init__(
        self, name: str, limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        """
        Return True if the visitor meets this slide's limitations,
        False otherwise.
        """
        try:
            self.limitation_class(
                age=visitor.age, weight=visitor.weight, height=visitor.height
            )
            return True
        except (ValueError, TypeError):
            return False
