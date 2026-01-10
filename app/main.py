from typing import Any, Type
from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError(f"{value} is not an integer")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"{value} is out of range "
                f"[{self.min_amount}, {self.max_amount}]"
            )
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.validate()

    @abstractmethod
    def validate(self) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def validate(self) -> None:
        self.age = self.age
        self.height = self.height
        self.weight = self.weight


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def validate(self) -> None:
        self.age = self.age
        self.height = self.height
        self.weight = self.weight


class Slide:
    name: str
    limitation_class: Type[SlideLimitationValidator]

    def __init__(
        self, name: str, limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                visitor.name, visitor.age, visitor.weight, visitor.height
            )
            return True
        except (TypeError, ValueError):
            return False
