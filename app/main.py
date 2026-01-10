from abc import ABC, abstractmethod
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> Any:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError
        setattr(instance, self.protected_name, value)

    def validate(self, value: int) -> bool:
        return (isinstance(value, int)
                and self.min_amount <= value <= self.max_amount)


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            height: int,
            weight: int
    ) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def validate(self) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def validate(self) -> bool:
        return (
            IntegerRange(4, 14).validate(self.age)
            and IntegerRange(80, 120).validate(self.height)
            and IntegerRange(20, 50).validate(self.weight)
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def validate(self) -> bool:
        return (
            IntegerRange(14, 60).validate(self.age)
            and IntegerRange(120, 220).validate(self.height)
            and IntegerRange(50, 120).validate(self.weight)
        )


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        validator = self.limitation_class(
            visitor.age, visitor.weight, visitor.height
        )
        return validator.validate()
