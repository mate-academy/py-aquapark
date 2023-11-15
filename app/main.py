from abc import ABC
from typing import Type, Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: Any, oven: Any) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if value > self.max_amount or value < self.min_amount:
            raise ValueError()
        setattr(instance, self.protected_name, value)

    def __set_name__(self, owner: Any, name: str) -> None:
        self.protected_name = "_" + name


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            weight: float,
            height: float
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: float, height: float) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age: int = IntegerRange(min_amount=4, max_amount=14)
    height: int = IntegerRange(min_amount=80, max_amount=120)
    weight: int = IntegerRange(min_amount=20, max_amount=50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age: int = IntegerRange(min_amount=14, max_amount=60)
    height: int = IntegerRange(min_amount=120, max_amount=220)
    weight: int = IntegerRange(min_amount=50, max_amount=120)


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
            self.limitation_class(visitor.age,
                                  visitor.weight,
                                  visitor.height)
            return True
        except ValueError:
            return False
