from typing import Any, Type


class IntegerRange:
    """Descriptor for parameter limitations."""

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Type, name: str) -> None:
        self.name = name
        self.private_name = "_" + name

    def __get__(self, instance: Any, owner: Type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance: Any, value: Any) -> None:
        # Check if value is an integer
        if not isinstance(value, int):
            raise TypeError(f"{self.name} must be an integer")

        # Check if value is within the allowed range (inclusive)
        if value < self.min_amount or value > self.max_amount:
            raise ValueError(
                f"{self.name} must be between "
                f"{self.min_amount} and {self.max_amount}"
            )

        setattr(instance, self.private_name, value)


class Visitor:
    """Class responsible for the user's personal data."""

    def __init__(
            self,
            name: str,
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator:
    """Base class for slide validators."""

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
    """Slide class with access validation."""

    def __init__(
            self,
            name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        """
        Check if a visitor can access the slide.

        Args:
            visitor: Visitor instance to check

        Returns:
            bool: True if visitor can access the slide, False otherwise
        """
        try:
            # Create an instance of the limitation validator
            # Pass visitor's parameters to the validator
            self.limitation_class(
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height
            )
            # If no exception was raised, the visitor can access
            return True
        except (TypeError, ValueError):
            # If validation failed, visitor cannot access
            return False
