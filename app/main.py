from typing import Type
from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Type, owner: Type) -> None:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: type, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        if value < self.min_amount or value > self.max_amount:
            raise ValueError
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            weight: int,
            height: int
    ):
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
    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)
        if not (4 <= age <= 14):
            raise ValueError("Age must be between 4 and 14 for children slide.")
        if not (80 <= height <= 120):
            raise ValueError("Height must be between 80 and 120 cm for children slide.")
        if not (20 <= weight <= 50):
            raise ValueError("Weight must be between 20 and 50 kg for children slide.")


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)
        if not (14 <= age <= 60):
            raise ValueError("Age must be between 14 and 60 for adult slide.")
        if not (120 <= height <= 220):
            raise ValueError("Height must be between 120 and 220 cm for adult slide.")
        if not (50 <= weight <= 120):
            raise ValueError("Weight must be between 50 and 120 kg for adult slide.")



class Slide:
    def __init__(self, name: str, limitation_class: Type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Type[Visitor]) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except ValueError:
            return False
