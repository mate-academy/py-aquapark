from abc import ABC, abstractmethod
from typing import Type


class IntegerRange:
    min_amount: int
    max_amount: int
    private_name: str

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, instance: object, owner: type) -> int:
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Only integers are allowed.")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"Value must be between {self.min_amount} and "
                f"{self.max_amount}"
            )
        setattr(instance, self.private_name, value)


class Visitor:
    name: str
    age: int
    weight: int
    height: int

    def __init__(self,
                 name: str,
                 age: int,
                 weight: int,
                 height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age: int,
                 weight: int,
                 height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height
        self.validate()

    @abstractmethod
    def validate(self) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def validate(self) -> None:
        self.age = self.age
        self.height = self.height
        self.weight = self.weight


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def validate(self) -> None:
        self.age = self.age
        self.height = self.height
        self.weight = self.weight


class Slide:
    name: str
    limitation_class: Type[SlideLimitationValidator]

    def __init__(self,
                 name: str,
                 limitation_class: Type[SlideLimitationValidator]
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except (TypeError, ValueError):
            return False
