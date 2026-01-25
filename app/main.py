from __future__ import annotations
from abc import ABC
from typing import Any, Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, instance: object, owner: Any) -> int:
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("The value should be integer.")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"The value should not be less than {self.min_amount} "
                f"and greater than {self.max_amount}."
            )
        setattr(instance, self.private_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    age = None
    height = None
    weight = None


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(self, name: str,
                 limitation_class: Type[ChildrenSlideLimitationValidator
                                        | AdultSlideLimitationValidator]
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        if not issubclass(self.limitation_class, SlideLimitationValidator):
            return False
        validate_instance = self.limitation_class()

        try:
            validate_instance.age = visitor.age
            validate_instance.height = visitor.height
            validate_instance.weight = visitor.weight
        except TypeError:
            print(f"Incorrect values for visitor {visitor.name}")
            return False
        except ValueError:
            print(f"The visitor {visitor.name} can't use the slide")
            return False

        return True
