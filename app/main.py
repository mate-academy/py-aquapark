from abc import ABC, abstractmethod
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: int) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.protected_name, value)
        else:
            raise ValueError


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):

    def __init__(self, age: int, weight: int, height: int) -> None:
        try:
            self.age = age
            self.weight = weight
            self.height = height
        except ValueError:
            pass

    @abstractmethod
    def validate(self, age: int, weight: int, height: int) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def validate(self, age: int, weight: int, height: int) -> bool:
        try:
            self.age = age
            self.weight = weight
            self.height = height
            return True
        except ValueError:
            return False


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def validate(self, age: int, weight: int, height: int) -> bool:
        try:
            self.age = age
            self.weight = weight
            self.height = height
            return True
        except ValueError:
            return False


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: Any) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class(
            visitor.age, visitor.weight, visitor.height
        ).validate(visitor.age, visitor.weight, visitor.height)
