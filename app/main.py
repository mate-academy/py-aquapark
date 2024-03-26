from __future__ import annotations

from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self,
                instance: type[SlideLimitationValidator],
                owner: SlideLimitationValidator) -> int | None:
        return getattr(instance, self.protected_name)

    def __set__(self,
                instance: type[SlideLimitationValidator],
                value: int) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("Value can only be int or float")
        elif not self.min_amount <= value <= self.max_amount:
            raise ValueError(f"The value of *{self.protected_name[1:]}* "
                             f"should be in range({self.min_amount} - "
                             f"{self.max_amount}). Yours ({value})")
        setattr(instance, self.protected_name, value)

    def __set_name__(self,
                     owner: SlideLimitationValidator,
                     name: str) -> None:
        self.protected_name = "_" + name


class Visitor:
    def __init__(self,
                 name: str,
                 age: int,
                 weight: int,
                 height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age: int,
                 weight: int,
                 height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


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
                 limitation_class: type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(age=visitor.age,
                                  height=visitor.height,
                                  weight=visitor.weight)
        except ValueError as e:
            print(e)
            return False
        return True
