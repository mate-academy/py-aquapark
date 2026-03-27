from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(
        self,
        owner: (
            "ChildrenSlideLimitationValidator",
            "AdultSlideLimitationValidator"
        ),
        name: str
    ) -> None:
        self.name = "_" + name

    def __get__(
        self,
        instance: (
            "ChildrenSlideLimitationValidator",
            "AdultSlideLimitationValidator"
        ),
        owner: Any
    ) -> int | None:
        return getattr(instance, self.name, None)

    def __set__(
        self,
        instance: (
            "ChildrenSlideLimitationValidator",
            "AdultSlideLimitationValidator"
        ),
        value: int
    ) -> None:
        if not isinstance(value, int):
            raise TypeError("Тип значення маэ бути int")
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.name, value)


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
    age = IntegerRange(min_amount=4, max_amount=14)
    height = IntegerRange(min_amount=80, max_amount=120)
    weight = IntegerRange(min_amount=20, max_amount=50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(min_amount=14, max_amount=60)
    height = IntegerRange(min_amount=120, max_amount=220)
    weight = IntegerRange(min_amount=50, max_amount=120)


class Slide:
    def __init__(
        self,
        name: str,
        limitation_class: (
            ChildrenSlideLimitationValidator,
            AdultSlideLimitationValidator
        )
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        valid = self.limitation_class(
            visitor.age,
            visitor.weight,
            visitor.height
        )
        return all([
            valid.age,
            valid.weight,
            valid.height
        ])
