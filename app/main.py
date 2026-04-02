from typing import Type, Any
from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.max_amount = max_amount
        self.min_amount = min_amount

    def __set_name__(self, owner: Type, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, instance: Any, owner: Type) -> None:
        value = getattr(instance, self.private_name)
        return value

    def __set__(self, obj: Any, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"{self.public_name} must be in the range"
                             f" [{self.min_amount}, {self.max_amount}]")
        setattr(obj, self.private_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.weight = weight
        self.age = age
        self.height = height
        self.name = name


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.height = height
        self.weight = weight
        self.age = age


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
        self.limitation_class = limitation_class
        self.name = name

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                age=visitor.age,
                height=visitor.height,
                weight=visitor.weight)
        except ValueError as e:
            print(e, visitor.height)
            return False
        return True
