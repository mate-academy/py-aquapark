from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(
            self,
            min_amount: int,
            max_amount: int
    ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: Any, owner: Any) -> Any:
        value = getattr(instance, self.protected_name)
        return value

    def __set__(self, instance: Any, value: Any) -> Any:
        if value < self.min_amount or value > self.max_amount:
            raise ValueError
        setattr(instance, self.protected_name, value)

    def __set_name__(self, owner: Any, name: str) -> Any:
        self.public_name = name
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
            limitation_class: type
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, person: Visitor) -> bool:
        try:
            self.limitation_class(person.age, person.weight, person.height)
        except ValueError:
            return False
        return True
