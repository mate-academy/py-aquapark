from abc import ABC
from dataclasses import dataclass
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: Any, owner: Any) -> int or None:
        if instance is not None:
            value = getattr(instance, self.name)
            return value
        return self

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Value should be integer, not {type(value)}")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"Value not in range [{self.min_amount},{self.max_amount}]"
            )
        setattr(instance, self.private_name, value)

    def __set_name__(self, owner: Any, name: Any) -> None:
        self.name = name
        self.private_name = f"_{name}"


@dataclass
class Visitor:

    name: str
    age: int
    weight: int
    height: int


class SlideLimitationValidator(ABC):
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
    age = IntegerRange(min_amount=4, max_amount=14)
    height = IntegerRange(min_amount=80, max_amount=120)
    weight = IntegerRange(min_amount=20, max_amount=50)

    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(min_amount=14, max_amount=60)
    height = IntegerRange(min_amount=120, max_amount=220)
    weight = IntegerRange(min_amount=50, max_amount=120)

    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
        super().__init__(age, weight, height)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        age_lm = self.limitation_class.age
        height_lm = self.limitation_class.height
        weight_lm = self.limitation_class.weight

        if (
            age_lm.min_amount <= visitor.age <= age_lm.max_amount
            and height_lm.min_amount <= visitor.height <= height_lm.max_amount
            and weight_lm.min_amount <= visitor.weight <= weight_lm.max_amount
        ):
            return True
        return False
