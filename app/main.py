from __future__ import annotations
from abc import ABC


class IntegerRange:

    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner: Visitor, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Visitor, owner: IntegerRange) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Visitor, value: int) -> None:
        if not self.min_value <= value <= self.max_value:
            return setattr(instance, self.protected_name, False)

        return setattr(instance, self.protected_name, True)


class Visitor:

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


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
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        current_visitor = self.limitation_class(
            visitor.age, visitor.weight, visitor.height
        )
        if all(
                [
                    current_visitor.age,
                    current_visitor.height,
                    current_visitor.weight
                ]
        ):
            return True
        return False
