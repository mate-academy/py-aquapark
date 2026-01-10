from abc import ABC
from typing import Any, Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: Any) -> None:
        self.private_name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> Any:
        return getattr(instance, self.private_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError()
        if value < self.min_amount or value > self.max_amount:
            raise ValueError()
        setattr(instance, self.private_name, value)


class Visitor:
    age = IntegerRange(0, 100)
    weight = IntegerRange(0, 200)
    height = IntegerRange(0, 300)

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
    age: int = IntegerRange(4, 14)
    weight: int = IntegerRange(20, 50)
    height: int = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age: int = IntegerRange(14, 60)
    weight: int = IntegerRange(50, 120)
    height: int = IntegerRange(120, 220)


class Slide:
    def __init__(self, name: str,
                 limitation_class: Type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            _ = self.limitation_class(visitor.age,
                                      visitor.weight,
                                      visitor.height)
            return True
        except (ValueError, TypeError):
            return False
