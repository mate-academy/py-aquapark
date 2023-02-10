from __future__ import annotations
from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(
            self,
            owner: SlideLimitationValidator,
            name: str
    ) -> None:
        self.protected_name = "_" + name

    def __get__(
            self,
            instance: SlideLimitationValidator,
            owner: SlideLimitationValidator
    ) -> None:
        return getattr(instance, self.protected_name)

    def __set__(
            self,
            instance: SlideLimitationValidator,
            value: int
    ) -> None:
        if self.min_amount <= value <= self.max_amount:
            return setattr(instance, self.protected_name, value)


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
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def set_age(self, value: int) -> None:
        pass

    @abstractmethod
    def set_weight(self, value: int) -> None:
        pass

    @abstractmethod
    def set_height(self, value: int) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def set_age(self, value: int) -> None:
        self.age = value

    def set_weight(self, value: int) -> None:
        self.weight = value

    def set_height(self, value: int) -> None:
        self.height = value


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def set_age(self, value: int) -> None:
        self.age = value

    def set_weight(self, value: int) -> None:
        self.weight = value

    def set_height(self, value: int) -> None:
        self.height = value


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator = None
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, other: Visitor) -> bool:
        if self.name == "Baby Slide":
            self.limitation_class = ChildrenSlideLimitationValidator(
                other.age,
                other.weight,
                other.height
            )
        else:
            self.limitation_class = AdultSlideLimitationValidator(
                other.age,
                other.weight,
                other.height
            )

        return True if len(self.limitation_class.__dict__) == 3 else False
