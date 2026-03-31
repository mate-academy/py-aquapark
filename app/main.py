from __future__ import annotations
from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: str, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: IntegerRange, owner: str) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: IntegerRange, value: int) -> None:
        setattr(
            instance,
            self.protected_name,
            value if self.min_amount <= value <= self.max_amount else None,
        )


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            weight: int,
            height: int,
    ) -> None:
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

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator,
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        person = self.limitation_class(
            age=visitor.age,
            weight=visitor.weight,
            height=visitor.height,
        )
        return all(
            [
                person.age is not None,
                person.weight is not None,
                person.height is not None,
            ]
        )
