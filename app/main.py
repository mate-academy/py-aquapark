from __future__ import annotations
from abc import ABC
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_value: int) -> None:
        self.min_amount = min_amount
        self.max_value = max_value

    def __set_name__(self, instance: Visitor, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Visitor, owner: Visitor) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Visitor, value: int) -> None:
        if not (self.min_amount <= value <= self.max_value):
            setattr(instance, self.protected_name, False)
        else:
            setattr(instance, self.protected_name, True)


class Visitor:
    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: Type[AdultSlideLimitationValidator]
            | Type[ChildrenSlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        limitation = self.limitation_class(
            visitor.age,
            visitor.height,
            visitor.weight
        )
        return all((limitation.age, limitation.height, limitation.weight))


adult_slide = Slide(
    name="Adult Slide", limitation_class=AdultSlideLimitationValidator
)
age = 60
height = 220
weight = 120
visitor = Visitor(name="User", age=age, height=height, weight=weight)
print(adult_slide.can_access(visitor))
