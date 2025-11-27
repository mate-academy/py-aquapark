from abc import ABC
from typing import Any, Optional


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(
        self, instance: Optional[object], owner: type
    ) -> Any:
        if instance is None:
            return self
        else:
            return instance.__dict__.get(self.name)

    def __set__(self, instance: object, value: Any) -> None:
        if isinstance(value, int):
            if self.min_amount <= value <= self.max_amount:
                instance.__dict__[self.name] = value
            else:
                raise ValueError
        else:
            raise TypeError

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name


class Visitor:
    def __init__(
        self, name: str, age: int, weight: float, height: float
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

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class Slide:
    def __init__(
        self, name: str, limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                visitor.age,
                int(visitor.weight),
                int(visitor.height)
            )
        except (TypeError, ValueError):
            return False
        return True
