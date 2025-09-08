from __future__ import annotations
from abc import ABC


class IntegerRange:
    def __init__(
            self: IntegerRange,
            min_amount: int,
            max_amount: int
    ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(
            self: IntegerRange,
            owner: SlideLimitationValidator,
            name: str
    ) -> None:
        self.protected_name = "_" + name

    def __set__(
            self: IntegerRange,
            instance: SlideLimitationValidator,
            value: int
    ) -> None:
        if not isinstance(value, int):
            raise TypeError()
        if value < self.min_amount or value > self.max_amount:
            raise ValueError()
        setattr(instance, self.protected_name, value)

    def __get__(
            self: IntegerRange,
            instance: SlideLimitationValidator,
            owner: SlideLimitationValidator
    ) -> int:
        return getattr(instance, self.protected_name)


class Visitor:
    def __init__(
            self: Visitor,
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
            self: SlideLimitationValidator,
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def __init__(
            self: ChildrenSlideLimitationValidator,
            age: int,
            weight: int,
            height: int
    ) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def __init__(
            self: AdultSlideLimitationValidator,
            age: int,
            weight: int,
            height: int
    ) -> None:
        super().__init__(age, weight, height)


class Slide:
    def __init__(
            self: Slide,
            name: str,
            limitation_class:
            ChildrenSlideLimitationValidator | AdultSlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, person: Visitor) -> bool:
        try:
            self.limitation_class(age=person.age,
                                  weight=person.weight,
                                  height=person.height)
            return True
        except (TypeError, ValueError):
            return False
