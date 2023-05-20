from abc import ABC
from typing import Any, Type


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self,
                instance: Type[SlideLimitationValidator],
                owner: Type[Any]) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self,
                instance: Type[SlideLimitationValidator],
                value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Should be integer")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"Value should be between {self.min_amount} "
                             f"and {self.max_amount}")
        setattr(instance, self.protected_name, value)

    def __set_name__(self, owner: Type[Any], name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name


class Visitor:
    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: Type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.height, visitor.weight)
        except ValueError:
            return False
        else:
            return True


# v = Visitor("Boba", 13, 360, 60)
# s = Slide("Mega", AdultSlideLimitationValidator)
# s.limitation_class.__init__( v.age, v.height, v.weight)
# print(s.limitation_class.__dict__)
# # print(s.__dict__["limitation_class"].__dict__)
