from __future__ import annotations
from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Visitor, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Visitor, owner: Visitor) -> Visitor:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Visitor, value: int) -> None:
        return setattr(instance, self.protected_name, value)


class Visitor:

    age = IntegerRange(4, 60)
    weight = IntegerRange(20, 120)
    height = IntegerRange(80, 220)

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
    def validate(self) -> bool:
        return (
            4 <= self.age <= 14
            and 80 <= self.height <= 120
            and 20 <= self.weight <= 50
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def validate(self) -> bool:
        return (
            14 <= self.age <= 60
            and 220 >= self.height
            >= 120 >= self.weight >= 50
        )


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: type(SlideLimitationValidator)
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, instance: Visitor) -> bool:
        return (
            self.limitation_class(
                instance.age,
                instance.weight,
                instance.height
            ).validate()
        )
