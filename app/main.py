from __future__ import annotations
from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(
            self,
            min_amount: int,
            max_amount: int
    ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(
            self,
            owner: SlideLimitationValidator,
            name: str
    ) -> None:
        self.protected_attr = "_" + name

    def __get__(
            self,
            instance: SlideLimitationValidator,
            owner: SlideLimitationValidator
    ) -> int:
        return getattr(instance, self.protected_attr)

    def __set__(
            self,
            instance: SlideLimitationValidator,
            value: int
    ) -> None:
        if value in range(self.min_amount, self.max_amount + 1):
            setattr(instance, self.protected_attr, value)
        else:
            setattr(instance, self.protected_attr, None)


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
    def validate(self) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def validate(self) -> bool:
        return True if self.age and self.weight and self.height else False


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def validate(self) -> bool:
        return True if self.age and self.weight and self.height else False


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(
            self,
            visitor: Visitor
    ) -> bool:
        if self.limitation_class == AdultSlideLimitationValidator:
            person = AdultSlideLimitationValidator(
                visitor.age, visitor.weight, visitor.height
            )
            return person.validate()
        person = ChildrenSlideLimitationValidator(
            visitor.age, visitor.weight, visitor.height
        )
        return person.validate()
