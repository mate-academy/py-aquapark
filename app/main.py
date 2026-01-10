from abc import ABC
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object, owner: object) -> int:
        return getattr(instance, self.protected_name)

    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = "_" + name

    def __set__(self,
                instance: object,
                value: int | float
                ) -> None:
        if not isinstance(value, int)\
                or not isinstance(value, float):
            raise TypeError()
        elif value < self.min_amount or value > self.max_amount:
            raise ValueError()
        else:
            setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self,
                 name: str,
                 age: int,
                 height: int | float,
                 weight: int | float
                 ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age: int,
                 height: int | float,
                 weight: int | float
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
    SlideValidatorType = (
        Type[ChildrenSlideLimitationValidator]
        | Type[AdultSlideLimitationValidator]
    )

    def __init__(self,
                 name: str,
                 limitation_class: SlideValidatorType
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        if issubclass(self.limitation_class, SlideLimitationValidator):
            try:
                self.limitation_class(visitor.age,
                                      visitor.height,
                                      visitor.weight
                                      )
                return True
            except (TypeError, ValueError):
                return False
        else:
            return False
