from __future__ import annotations
from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, max_amount: int, min_amount: int) -> None:
        self.max_amount = max_amount
        self.min_amount = min_amount

    def __set_name__(self, owner: Visitor, name) -> str:
        self.name = name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance: Visitor, value: int) -> None:
        if self.max_amount < value or value < self.min_amount:
            raise ValueError(f"{self.name} has_access "
                             f"for visitor with such parameters:"
                             f" (age: {instance.age},weight: {instance.weight}"
                             f"height: {instance.height}. ")
        else:
            setattr(instance, self.name, value)

class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int,
            weight: int,
            height: int,
    ):
        self.age = age
        self.weight = weight
        self.height = height

class ChildrenSlideLimitationValidator(
SlideLimitationValidator
):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)
        self.age = age
        self.weight = weight
        self.height = height


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)



class Slide:
    def __init__(
            self, name: str, limitation_class: SlideLimitationValidator

    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor):
        limitation_class = SlideLimitationValidator(visitor.age, visitor.height, visitor.weight )
        try:
            if visitor != limitation_class:
                return False
            elif visitor == limitation_class:
                return True
        except ValueError:
            print("unknown error")

