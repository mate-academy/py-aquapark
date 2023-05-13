from abc import ABC
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Type, owner: Type) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Type, value: int) -> None:
        if isinstance(value, int):
            if self.min_amount <= value <= self.max_amount:
                setattr(instance, self.protected_name, value)
                return
            else:
                raise ValueError


class Visitor:
    age = IntegerRange(4, 60)
    height = IntegerRange(80, 220)
    weight = IntegerRange(20, 120)

    def __init__(
            self, name: str, age: int, height: int, weight: int
    ) -> None:
        self._name = name
        self._age = age
        self._height = height
        self._weight = weight


class SlideLimitationValidator(ABC):
    def __init__(
            self, age: int, height: int, weight: int
    ) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, height: int, weight: int) -> None:
        super().__init__(age, height, weight)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, height: int, weight: int) -> None:
        super().__init__(age, height, weight)


class Slide:
    def __init__(
            self, name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.height, visitor.weight)
            return True
        except ValueError:
            return False
