from __future__ import annotations
from typing import Any
from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.name = name
        self.protected_name = "_" + name

    def __get__(self, instance: Visitor, owner: Any) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Visitor, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            height: int | float,
            weight: int | float,
    ) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int,
            height: int | float,
            weight: int | float
    ) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator, ABC):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator, ABC):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.height, visitor.weight)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    visitor = Visitor(name="John", age=14, height=120, weight=50)
    adult_slide = Slide(name="Adult-slide",
                        limitation_class=AdultSlideLimitationValidator)

    # Now, test if the visitor can access the slide
    print(adult_slide.can_access(visitor))
