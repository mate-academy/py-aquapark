from abc import ABC


class IntegerRange:
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def contains(self, value: int) -> bool:
        return self.min_value <= value <= self.max_value


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
    def is_valid(cls, visitor: Visitor) -> bool:
        return (
            cls.age_range.contains(visitor.age)
            and cls.height_range.contains(visitor.height)
            and cls.weight_range.contains(visitor.weight)
        )


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
        limitation_class: type[SlideLimitationValidator],
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.is_valid(visitor)
