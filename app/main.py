from abc import ABC
from typing import Any, Optional, Type


class IntegerRange:
    """Descriptor for validating integer values within a specified range.

    This descriptor ensures that the assigned value is an integer and falls
    within the defined minimum and maximum bounds.

    Attributes:
        min_amount: The minimum acceptable integer value.
        max_amount: The maximum acceptable integer value.
        protected_name: The name of the protected attribute to store the value.
    """

    def __init__(self, min_amount: int, max_amount: int) -> None:
        """Initialize the IntegerRange descriptor.

        Args:
            min_amount: The minimum acceptable integer value.
            max_amount: The maximum acceptable integer value.
        """
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Type, name: str) -> None:
        """Store the name of the attribute being described.

        Args:
            owner: The class that owns this descriptor.
            name: The name of the attribute in the owner class.
        """
        self.protected_name = f"_{name}"

    def __get__(self, instance: Optional[Any], owner: Type) -> Any:
        """Retrieve the value of the descriptor.

        Args:
            instance: The instance of the owner class, or None if accessed
                from the class itself.
            owner: The owner class.

        Returns:
            The descriptor itself if accessed from the class, otherwise
            the stored value.
        """
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: int) -> None:
        """Set and validate the value of the descriptor.

        Args:
            instance: The instance of the owner class.
            value: The value to be set.

        Raises:
            TypeError: If the value is not an integer.
            ValueError: If the value is outside the allowed range.
        """
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"Value must be between {self.min_amount} "
                f"and {self.max_amount}"
            )
        setattr(instance, self.protected_name, value)


class Visitor:
    """Represents a visitor to the aqua-park.

    This class stores visitor information without any limitations or
    validation constraints.

    Attributes:
        name: The visitor's name.
        age: The visitor's age in years.
        weight: The visitor's weight in kilograms.
        height: The visitor's height in centimeters.
    """

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        """Initialize a Visitor instance.

        Args:
            name: The visitor's name.
            age: The visitor's age in years.
            weight: The visitor's weight in kilograms.
            height: The visitor's height in centimeters.
        """
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    """Abstract base class for slide limitation validators.

    This class provides a common structure for validators that check
    whether a visitor meets the requirements to use a specific slide.

    Attributes:
        age: The visitor's age to validate.
        weight: The visitor's weight to validate.
        height: The visitor's height to validate.
    """

    def __init__(self, age: int, weight: int, height: int) -> None:
        """Initialize a SlideLimitationValidator instance.

        Args:
            age: The visitor's age in years.
            weight: The visitor's weight in kilograms.
            height: The visitor's height in centimeters.
        """
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    """Validator for children's slide limitations.

    This validator enforces the following restrictions:
    - Age: 4-14 years
    - Height: 80-120 cm
    - Weight: 20-50 kg

    Attributes:
        age: IntegerRange descriptor for age validation.
        height: IntegerRange descriptor for height validation.
        weight: IntegerRange descriptor for weight validation.
    """

    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    """Validator for adult slide limitations.

    This validator enforces the following restrictions:
    - Age: 14-60 years
    - Height: 120-220 cm
    - Weight: 50-120 kg

    Attributes:
        age: IntegerRange descriptor for age validation.
        height: IntegerRange descriptor for height validation.
        weight: IntegerRange descriptor for weight validation.
    """

    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    """Represents a slide in the aqua-park with access limitations.

    This class manages slide information and determines whether a visitor
    can access the slide based on the specified limitation validator.

    Attributes:
        name: The name of the slide.
        limitation_class: The validator class used to check
        visitor eligibility.
    """

    def __init__(
            self,
            name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        """Initialize a Slide instance.

        Args:
            name: The name of the slide.
            limitation_class: A SlideLimitationValidator subclass that defines
                the restrictions for using this slide.
        """
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        """Check if a visitor can access the slide.

        This method creates an instance of the limitation_class with the
        visitor's parameters and catches any validation errors that may occur.

        Args:
            visitor: The Visitor instance to validate.

        Returns:
            True if the visitor meets all requirements, False otherwise.
        """
        try:
            self.limitation_class(
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height
            )
            return True
        except (TypeError, ValueError):
            return False
