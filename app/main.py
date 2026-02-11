from __future__ import annotations
from abc import ABC


class IntegerRange:
    """A descriptor to validate if an integer falls within a specified range.

    :param min_amount: The minimum allowed integer value.
    :type min_amount: int
    :param max_amount: The maximum allowed integer value.
    :type max_amount: int
    """
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(
            self,
            owner: type[SlideLimitationValidator],
            name: str
    ) -> None:
        """Sets the protected name for the attribute.

        :param owner: The class that owns this descriptor.
        :type owner: type[SlideLimitationValidator]
        :param name: The name of the attribute in the owner class.
        :type name: str
        """
        self.protected_name = "_" + name

    def __get__(
            self,
            instance: SlideLimitationValidator,
            owner: type[SlideLimitationValidator],
    ) -> int:
        """Retrieves the value of the attribute.

        :param instance: The instance of the owner class.
        :type instance: SlideLimitationValidator
        :param owner: The class that owns this descriptor.
        :type owner: type[SlideLimitationValidator]
        :returns: The value of the attribute.
        :rtype: int
        """
        return getattr(instance, self.protected_name)

    def __set__(
            self,
            instance: SlideLimitationValidator,
            value: int
    ) -> None:
        """Sets the value of the attribute after validation.

        :param instance: The instance of the owner class.
        :type instance: SlideLimitationValidator
        :param value: The value to be set.
        :type value: int
        :raises TypeError: If the value is not an integer.
        :raises ValueError: If the value is outside the specified range.
        """
        if not isinstance(value, int):
            raise TypeError()
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError()
        setattr(instance, self.protected_name, value)


class Visitor:
    """Represents a visitor to the aquapark.

    :param name: The name of the visitor.
    :type name: str
    :param age: The age of the visitor.
    :type age: int
    :param weight: The weight of the visitor in kg.
    :type weight: int
    :param height: The height of the visitor in cm.
    :type height: int
    """
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


class SlideLimitationValidator(ABC):
    """Abstract base class for slide limitation validators.

    :param age: The age limit.
    :type age: int
    :param weight: The weight limit.
    :type weight: int
    :param height: The height limit.
    :type height: int
    """
    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    """Validator for children's slides, defining specific age, weight,
    and height ranges.
    """
    age: IntegerRange = IntegerRange(4, 14)
    weight: IntegerRange = IntegerRange(20, 50)
    height: IntegerRange = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    """Validator for adult slides, defining specific age, weight,
    and height ranges.
    """
    age: IntegerRange = IntegerRange(14, 60)
    weight: IntegerRange = IntegerRange(50, 120)
    height: IntegerRange = IntegerRange(120, 220)


class Slide:
    """Represents a slide in the aquapark with specific access limitations.

    :param name: The name of the slide.
    :type name: str
    :param limitation_class: The validator class used to check access.
    :type limitation_class: type[SlideLimitationValidator]
    """
    def __init__(
            self,
            name: str,
            limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(
            self,
            visitor: Visitor
    ) -> bool:
        """Checks if a visitor can access the slide based on its limitations.

        :param visitor: The visitor attempting to access the slide.
        :type visitor: Visitor
        :returns: True if the visitor can access, False otherwise.
        :rtype: bool
        """
        try:
            self.limitation_class(
                visitor.age,
                visitor.weight,
                visitor.height
            )
            return True
        except (ValueError, TypeError):
            return False
