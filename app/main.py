from abc import ABC
from typing import Any, Optional, Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Type[Any], name: Any) -> None:
        self.name = name

    def __get__(self, instance: Optional[Type], owner: Type[Any]) -> Any:
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance: Optional[Type], value: Any) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError
        if value < self.min_amount or value > self.max_amount:
            raise ValueError
        instance.__dict__[self.name] = value


class Visitor:
    def __init__(self,
                 name: str,
                 age: int,
                 weight: int | float,
                 height: int | float
                 ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age: int,
                 weight: int | float,
                 height: int | float
                 ) -> None:
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
    def __init__(self,
                 name: str,
                 limitation_class: SlideLimitationValidator
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except (ValueError, TypeError):
            return False
