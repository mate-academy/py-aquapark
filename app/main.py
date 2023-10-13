from __future__ import annotations
from abc import ABC
from typing import Union, Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(
            self,
            instance: Visitor,
            owner: Type[Visitor]
    ) -> Union[str, int]:
        return getattr(instance, self.private_name)

    def __set__(self, instance: Visitor, value: int):
        if not isinstance(value, int):
            raise TypeError('Value must be an integer')
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f'Value must be in range '
                f'{self.min_amount}-{self.max_amount}'
            )
        setattr(instance, self.private_name, value)

    def __set_name__(self, owner: Visitor, name: str) -> None:
        self.private_name = "_" + name


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
    age: IntegerRange = IntegerRange(4, 14)
    weight: IntegerRange = IntegerRange(20, 50)
    height: IntegerRange = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age: IntegerRange = IntegerRange(14, 60)
    weight: IntegerRange = IntegerRange(50, 120)
    height: IntegerRange = IntegerRange(120, 220)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except ValueError:
            return False
