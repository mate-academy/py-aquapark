from abc import ABC
from typing import Type, Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Any, owner: Type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError()
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
    def __init__(
            self,
            age: IntegerRange,
            weight: IntegerRange,
            height: IntegerRange
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def __init__(self) -> None:
        pass


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def __init__(self) -> None:
        pass


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: Type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        validator = self.limitation_class()
        try:
            validator.age = visitor.age
            validator.weight = visitor.weight
            validator.height = visitor.height
        except (TypeError, ValueError):
            return False
        return True
