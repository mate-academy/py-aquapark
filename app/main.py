from __future__ import annotations

from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, obj: Any, objtype: Any = None) -> None:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: Any, value: Any) -> None:
        setattr(obj, self.protected_name, value)


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
    def __init__(self) -> None:
        super().__init__(
            age=IntegerRange(4, 14),
            weight=IntegerRange(20, 50),
            height=IntegerRange(80, 120)
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):

    def __init__(self) -> None:
        super().__init__(
            age=IntegerRange(14, 60),
            weight=IntegerRange(50, 120),
            height=IntegerRange(120, 220)
        )


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class:
            AdultSlideLimitationValidator | ChildrenSlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        slide = self.limitation_class

        return all([
            slide.age.min_amount
            <= visitor.age
            <= slide.age.max_amount,

            slide.weight.min_amount
            <= visitor.weight
            <= slide.weight.max_amount,

            slide.height.min_amount
            <= visitor.height
            <= slide.height.max_amount
        ])
