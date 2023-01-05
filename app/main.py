from __future__ import annotations
from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: any, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, obj: any, objtype: any = None) -> None:
        value = getattr(obj, self.private_name)
        return value

    def __set__(self, obj: any, value: any) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be integer!")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"Quantity should not be less than {self.min_amount}"
                f" and greater than {self.max_amount}."
            )
        setattr(obj, self.private_name, value)


class Visitor:

    def __init__(
            self,
            name: str,
            age: int,
            weight: int,
            height: int
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
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)


class Slide:

    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        result = []
        try:
            self.limitation_class(
                visitor.age,
                visitor.weight,
                visitor.height
            )
        except ValueError or TypeError:
            result.append(False)
        else:
            result.append(True)
        return any(result)
