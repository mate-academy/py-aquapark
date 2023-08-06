from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def validate(self, value: int) -> bool:
        return self.min_amount <= value <= self.max_amount


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    @abstractmethod
    def can_access(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def can_access(self, visitor: Visitor) -> bool:
        try:
            return (
                4 <= visitor.age <= 14
                and 20 <= visitor.weight <= 50
                and 80 <= visitor.height <= 120
            )
        except ValueError:
            return False


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def can_access(self, visitor: Visitor) -> bool:
        try:
            return (
                14 <= visitor.age <= 60
                and 50 <= visitor.weight <= 120 <= visitor.height <= 220
            )
        except ValueError:
            return False


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_validator = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_validator.can_access(visitor)
