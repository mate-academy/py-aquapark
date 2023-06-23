from abc import ABC
from typing import Any, Callable


class IntegerRange:

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Callable, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance: Callable, owner: Callable) -> Any:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Callable, value: Any) -> None:
        if value in range(self.min_amount, self.max_amount + 1):
            setattr(instance, self.protected_name, value)


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

    def __init__(self, age: int, weight: int, height: int) -> None:
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
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, instance: Visitor) -> bool:
        return len(
            self.limitation_class(
                instance.age,
                instance.weight,
                instance.height
            ).__dict__) == 3
