from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def validate(self, value: int) -> None:
        if value < self.min_amount or value > self.max_amount:
            raise ValueError(
                f"Value {value}"
                f" is out of range ({self.min_amount}, {self.max_amount})"
            )


class Visitor:
    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    age_range: IntegerRange
    height_range: IntegerRange
    weight_range: IntegerRange

    @classmethod
    def can_access(cls, visitor: Visitor) -> bool:
        try:
            cls.age_range.validate(visitor.age)
            cls.height_range.validate(visitor.height)
            cls.weight_range.validate(visitor.weight)
            return True
        except ValueError:
            return False


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age_range = IntegerRange(4, 14)
    height_range = IntegerRange(80, 120)
    weight_range = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age_range = IntegerRange(14, 60)
    height_range = IntegerRange(120, 220)
    weight_range = IntegerRange(50, 120)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.can_access(visitor)
