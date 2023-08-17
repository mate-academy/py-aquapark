from abc import ABC
from typing import Generic, Type, TypeVar

Instance = TypeVar("Instance")
Value = TypeVar("Value")


class IntegerRange(Generic[Instance, Value]):
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount: int = min_amount
        self.max_amount: int = max_amount

    def __set_name__(self, _: Instance, name: str) -> None:
        self.public_name: str = name
        self.protected_name: str = "_" + name

    def __get__(self, instance: Instance, _: Type[Instance]) -> Value:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Instance, value: Value) -> None:
        if value not in range(self.min_amount, self.max_amount + 1):
            raise ValueError(
                f"{self.public_name} has to be in the range "
                f"{self.min_amount}..{self.max_amount}"
            )
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(
        self, name: str, age: int, weight: float, height: float
    ) -> None:
        self.name: str = name
        self.age: int = age
        self.weight: float = weight
        self.height: float = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: float, height: float) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)


class Slide:
    def __init__(
        self, name: str, limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name: str = name
        self.limitation_class: Type[
            SlideLimitationValidator
        ] = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
        except ValueError:
            return False
        return True
