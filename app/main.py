from abc import ABC, abstractmethod
from typing import Optional, Type


class IntegerRange:
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value: int = min_value
        self.max_value: int = max_value

    def __get__(self, instance: Optional[object],
                owner: Type) -> Optional[int]:
        return instance.__dict__.get(self._name) if instance else None

    def __set__(self, instance: object, value: int) -> None:
        if (value < self.min_value
                or value > self.max_value):
            raise ValueError(f"Value {value} "
                             f"is out of range ({self.min_value}, "
                             f"{self.max_value})")
        instance.__dict__[self._name] = value

    def __set_name__(self, owner: Type, name: str) -> None:
        self._name = name


class SlideLimitationValidator(ABC):
    @abstractmethod
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age: int = age
        self.weight: int = weight
        self.height: int = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age: IntegerRange
    height: IntegerRange
    weight: IntegerRange

    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age: IntegerRange
    height: IntegerRange
    weight: IntegerRange

    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name: str = name
        self.age: int = age
        self.weight: int = weight
        self.height: int = height


class Slide:
    def __init__(self, name: str,
                 limitation_class:
                 Type[SlideLimitationValidator]) -> None:
        self.name: str = name
        self.limitation_class: (
            Type)[SlideLimitationValidator] = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except ValueError:
            return False
