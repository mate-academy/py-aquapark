from abc import ABC, abstractmethod
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, instance: object, owner: type) -> int:
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"Value {value} out of range ({self.min_amount},"
                f" {self.max_amount})"
            )
        setattr(instance, self.private_name, value)


class Visitor:
    age = IntegerRange(0, 150)
    weight = IntegerRange(0, 300)
    height = IntegerRange(0, 300)

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age_range: tuple,
            weight_range: tuple,
            height_range: tuple
    ) -> None:
        self.age_range = age_range
        self.weight_range = weight_range
        self.height_range = height_range

    def _validate_ranges(self, visitor: "Visitor") -> bool:
        return (
            self.age_range[0] <= visitor.age <= self.age_range[1]
            and self.weight_range[0] <= visitor.weight <= self.weight_range[1]
            and self.height_range[0] <= visitor.height <= self.height_range[1]
        )

    @abstractmethod
    def validate(self, visitor: "Visitor") -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__((4, 14), (20, 50), (80, 120))

    def validate(self, visitor: "Visitor") -> bool:
        return self._validate_ranges(visitor)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__((14, 60), (50, 120), (120, 220))

    def validate(self, visitor: "Visitor") -> bool:
        return self._validate_ranges(visitor)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_validator = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_validator.validate(visitor)
