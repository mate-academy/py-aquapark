from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: int, owner: str) -> tuple:
        return self.min_amount, self.max_amount

    def __set__(self, instance: int, value: int) -> None:
        raise AttributeError("Cannot set value directly")

    def __set_name__(self, owner: str, name: str) -> None:
        self.name = name


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
        self.age_range = age
        self.weight_range = weight
        self.height_range = height

    @abstractmethod
    def can_access(self, visitor: Visitor) -> bool:
        pass


def can_access(self: SlideLimitationValidator, visitor: Visitor) -> bool:
    return (
        self.age_range.min_amount <= visitor.age
        <= self.age_range.max_amount and self.height_range.min_amount
        <= visitor.height
        <= self.height_range.max_amount and self.weight_range.min_amount
        <= visitor.weight <= self.weight_range.max_amount
    )


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age = IntegerRange(4, 14)
        height = IntegerRange(80, 120)
        weight = IntegerRange(20, 50)
        super().__init__(age, weight, height)

    can_access = can_access


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age = IntegerRange(14, 60)
        height = IntegerRange(120, 220)
        weight = IntegerRange(50, 120)
        super().__init__(age, weight, height)

    can_access = can_access


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_validator = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_validator.can_access(visitor)
