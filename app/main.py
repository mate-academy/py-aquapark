from abc import ABC
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object = None, owner: Type = None) -> bool:
        return self.value

    def __set__(self, instance: object, value: bool = True) -> None:
        self.value = value
        limitation_ranges = {
            ChildrenSlideLimitationValidator: ChildrenSlideLimitationValidator.
            children_slide_limitation_validator,
            AdultSlideLimitationValidator: AdultSlideLimitationValidator.
            adult_slide_limitation_validator,
        }

        limitation_range = limitation_ranges.get(self.limitation_class)

        if (
            not (limitation_range["age"][0] <= self.age
                 <= limitation_range["age"][1])
            or not (limitation_range["height"][0] <= self.height
                    <= limitation_range["height"][1])
            or not (limitation_range["weight"][0] <= self.weight
                    <= limitation_range["weight"][1])
        ):
            self.value = False
        else:
            self.value = True


class Visitor:
    def __init__(
            self, age: int, height: int, weight: int,
            name: str = ""
    ) -> None:
        self.age = age
        self.height = height
        self.weight = weight
        self.name = name


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    children_slide_limitation_validator = {
        "age": (4, 14),
        "height": (80, 120),
        "weight": (20, 50)
    }


class AdultSlideLimitationValidator(SlideLimitationValidator):
    adult_slide_limitation_validator = {
        "age": (14, 60),
        "height": (120, 220),
        "weight": (50, 120)
    }


class Slide:
    def __init__(self, name: str, limitation_class: int,) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor, value: bool = True) -> bool:
        self.age = visitor.age
        self.height = visitor.height
        self.weight = visitor.weight
        IntegerRange.__set__(self, value)
        return IntegerRange.__get__(self)
