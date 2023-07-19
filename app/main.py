from abc import ABC, abstractmethod
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: "Slide", owner: Type) -> str:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: "Slide", value: int) -> None:
        if type(value) is not int:
            raise TypeError("Value should be integer")
        if value < self.min_amount or value > self.max_amount:
            setattr(instance, self.protected_name, False)
        else:
            setattr(instance, self.protected_name, True)


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
    @abstractmethod
    def __init__(self, age: int, height: int, weight: int) -> None:
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
            self, name: str, limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        if False in self.limitation_class(
                visitor.age, visitor.height, visitor.weight
        ).__dict__.values():
            return False
        return True
