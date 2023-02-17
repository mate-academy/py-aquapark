from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.name = name
        self.protected_name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> str | int | bool:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        setattr(instance, self.protected_name, value)
        if not self.min_amount <= value <= self.max_amount:
            setattr(instance, self.protected_name, False)


class Visitor:
    age = IntegerRange(4, 60)
    weight = IntegerRange(20, 120)
    height = IntegerRange(80, 220)

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self._name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    def check_access(self) -> bool:
        return all([self.age, self.weight, self.height])


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
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        return (
            self.limitation_class(
                visitor.age,
                visitor.weight,
                visitor.height
            ).check_access()
        )
