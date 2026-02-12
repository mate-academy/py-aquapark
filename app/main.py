from abc import ABC
from typing import Any, Type, Optional


class IntegerRange:
    """
    Descriptor to validate visitor parameter ranges.
    """

    def __init__(
        self,
        min_amount: int,
        max_amount: int
    ) -> None:
        """
        Initializes the range limits.

        Args:
            min_amount: Minimum allowed integer value.
            max_amount: Maximum allowed integer value.
        """
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(
        self,
        owner: object,
        name: str
    ) -> None:
        """
        Assigns the protected name to the attribute.

        Args:
            owner: The class where the descriptor is defined.
            name: The name of the attribute.
        """
        self.private_name = "_" + name

    def __get__(
        self,
        obj: Optional[object],
        objtype: Optional[Type] = None
    ) -> Any:
        """
        Returns the value of the attribute from the instance.

        Args:
            obj: The instance of the object (Visitor).
            objtype: The type of the class.

        Returns:
            The stored value or the instance of the descriptor if obj is  None.
        """
        if obj is None:
            return self
        return getattr(obj, self.private_name)

    def __set__(
        self,
        obj: object,
        value: int
    ) -> None:
        """
        Validates and assigns the value.

        Args:
            obj: Visitor instance.
            value: Value to validate.

        Raises:
            TypeError: If the value is not an integer.
            ValueError: If the value is out of range.
        """
        if not isinstance(value, int):
            raise TypeError
        elif value < self.min_amount or value > self.max_amount:
            raise ValueError
        setattr(obj, self.private_name, value)


class Visitor:
    """
    Keep the personal data of each visitor.
    """

    def __init__(
        self,
        name: str,
        age: int,
        weight: int,
        height: int
    ) -> None:
        """
        Initializes the information of the visitor.

        Args:
            name: the name of the visitor.
            age: how old they are.
            weight: weight rounded to integers.
            height: height rounded to integers.
        """
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    """
    Base class for slide limitation validators.

    This class serves as a container for age, weight, and height
        constraints that a visitor must meet to use a slide.
    """

    def __init__(
        self,
        age: int,
        weight: int,
        height: int
    ) -> None:
        """
        Initializes the limitation validator with specific constraints.

        Args:
            age: The required age value or range validator.
            weight: The required weight value or range validator.
            height: The required height value or range validator.
        """
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    """
    Validator for children's slides.

    Uses IntegerRange descriptors to enforce specific constraints 
        for younger visitors.

    Attributes:
        age (IntegerRange): Restricted to 4-14 years.
        weight (IntegerRange): Restricted to 20-50 kg.
        height (IntegerRange): Restricted to 80-120 cm.
    """
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    pass


class Slide:
    pass
