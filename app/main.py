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
    pass


class SlideLimitationValidator(ABC):
    pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    pass


class AdultSlideLimitationValidator(SlideLimitationValidator):
    pass


class Slide:
    pass
