from abc import ABC
from typing import Callable
from typing import Union


class IntegerRange:
    def __init__(self, min_amount: int = None, max_amount: int = None) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Callable, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self,
                instance: Callable,
                owner: Callable) -> Union[int, float]:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Callable, value: Union[int, float]) -> bool:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError()
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
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
    weight = IntegerRange(80, 120)
    height = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(120, 220)
    height = IntegerRange(50, 120)


class Slide:
    def __init__(self, name: str, limitation_class: Callable) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.height, visitor.weight)
        except ValueError:
            return False
        return True
