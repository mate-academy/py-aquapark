from __future__ import annotations
from typing import Any

from abc import abstractmethod, ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> int:
        return getattr(instance, self.name)

    def __set__(self, instance: Any, value: int) -> None:
        # if not self.min_amount <= value <= self.max_amount:
        #     raise ValueError
        setattr(instance, self.name, value)


class Visitor:

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: IntegerRange,
            weight: IntegerRange,
            height: IntegerRange
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            IntegerRange(4, 14),
            IntegerRange(20, 50),
            IntegerRange(80, 120)
        )

    def validate(self, visitor: Visitor) -> bool:
        return all([
            self.age.min_amount <= visitor.age <= self.age.max_amount,
            self.height.min_amount <= visitor.height <= self.height.max_amount,
            self.weight.min_amount <= visitor.weight <= self.weight.max_amount
        ])


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            IntegerRange(14, 60),
            IntegerRange(50, 120),
            IntegerRange(120, 220))
    # age = IntegerRange(14, 60)
    # height = IntegerRange(120, 220)
    # weight = IntegerRange(50, 120)

    def validate(self, visitor: Visitor) -> bool:
        return all([
            self.age.min_amount <= visitor.age <= self.age.max_amount,
            self.height.min_amount <= visitor.height <= self.height.max_amount,
            self.weight.min_amount <= visitor.weight <= self.weight.max_amount
        ])


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.validate(visitor)
        # try:
        #     self.limitation_class.age = visitor.age
        #     self.limitation_class.weight = visitor.weight
        #     self.limitation_class.height = visitor.height
        #     return True
        # except ValueError:
        #     return False
