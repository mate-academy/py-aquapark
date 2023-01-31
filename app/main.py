from __future__ import annotations
from abc import ABC


class IntegerRange:

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(
            self,
            owner: ChildrenSlideLimitationValidator
            | AdultSlideLimitationValidator,
            name: str
    ) -> None:
        self.protect_name = "_" + name

    def __get__(
            self,
            instance: ChildrenSlideLimitationValidator
            | AdultSlideLimitationValidator,
            owner: ChildrenSlideLimitationValidator
            | AdultSlideLimitationValidator
    ) -> int:
        return getattr(instance, self.protect_name)

    def __set__(
            self,
            instance: ChildrenSlideLimitationValidator
            | AdultSlideLimitationValidator,
            value: int
    ) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.protect_name, value)
        else:
            value = 0
            setattr(instance, self.protect_name, value)


class Visitor:

    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):

    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:

    def __init__(
            self,
            name: str,
            limitation_class: ChildrenSlideLimitationValidator
            | AdultSlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:

        if self.limitation_class.__name__ ==\
                "ChildrenSlideLimitationValidator":
            validator_dict = ChildrenSlideLimitationValidator(
                visitor.age,
                visitor.height,
                visitor.weight
            )
            if validator_dict.age > 0\
                    and validator_dict.weight > 0\
                    and validator_dict.height > 0:
                return True
            else:
                return False

        if self.limitation_class.__name__ == "AdultSlideLimitationValidator":
            validator_dict = AdultSlideLimitationValidator(
                visitor.age,
                visitor.height,
                visitor.weight
            )
            if validator_dict.age > 0\
                    and validator_dict.weight > 0\
                    and validator_dict.height > 0:
                return True
            else:
                return False
