from abc import ABC, abstractmethod
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer.")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"Value must be between {self.min_amount}"
                f" and {self.max_amount}."
            )
        setattr(instance, self.private_name, value)


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
    age = IntegerRange(0, 200)
    weight = IntegerRange(0, 500)

    def __init__(
        self,
        age: int,
        weight: int,
        height: int
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def validate(self) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def validate(self) -> None:
        pass


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def validate(self) -> None:
        pass


class Slide:
    def __init__(
        self,
        name: str,
        limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            validator = self.limitation_class(
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height
            )
            validator.validate()
            return True
        except (TypeError, ValueError):
            return False
