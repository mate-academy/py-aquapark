from abc import ABC
from typing import Type


class IntegerRange:
    def __init__(
            self,
            min_amount: int,
            max_amount: int
    ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object, owner: Type) -> int:
        return getattr(instance, self.name)

    def __set__(self, instance: object, value: int) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.protected_name, value)
        else:
            raise ValueError(f"{self.protected_name} should be "
                             f"between {self.min_amount} and "
                             f"{self.max_amount}")

    def __set_name__(self, owner: Type, name: str) -> None:
        self.protected_name = "_" + name


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
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_validator = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_validator(age=visitor.age,
                                      height=visitor.height,
                                      weight=visitor.weight)
            return True
        except ValueError:
            return False
