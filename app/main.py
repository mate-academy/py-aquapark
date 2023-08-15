from abc import ABC, abstractmethod
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.name = name
        self.protected_name = f"_{name}"

    def __get__(self, instance: Any, owner: Any) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: int) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.protected_name, value)
        else:
            raise ValueError(
                f"Value must be between "
                f"{self.min_amount} and {self.max_amount}"
            )


class Visitor:
    age: int = IntegerRange(0, 120)
    weight: int = IntegerRange(0, 300)
    height: int = IntegerRange(0, 300)

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
        self, age: IntegerRange, weight: IntegerRange, height: IntegerRange
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
            age=IntegerRange(4, 14),
            weight=IntegerRange(20, 50),
            height=IntegerRange(80, 120),
        )

    def validate(self, visitor: Visitor) -> bool:
        return all(
            [
                self.age.min_amount <= visitor.age <= self.age.max_amount,
                self.weight.min_amount
                <= visitor.weight
                <= self.weight.max_amount,
                self.height.min_amount
                <= visitor.height
                <= self.height.max_amount,
            ]
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            age=IntegerRange(14, 60),
            weight=IntegerRange(50, 120),
            height=IntegerRange(120, 220),
        )

    def validate(self, visitor: Visitor) -> bool:
        return all(
            [
                self.age.min_amount <= visitor.age <= self.age.max_amount,
                self.weight.min_amount
                <= visitor.weight
                <= self.weight.max_amount,
                self.height.min_amount
                <= visitor.height
                <= self.height.max_amount,
            ]
        )


class Slide:
    def __init__(
        self, name: str, limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.validate(visitor)
