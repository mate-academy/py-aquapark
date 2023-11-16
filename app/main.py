from abc import ABC


class IntegerRange:
    def __init__(self, min_amount, max_amount) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, obj, instance) -> None:
        return getattr(obj, '_value')

    def __set__(self, obj, value) -> None:
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(f"Value {value} is not within the range {self.min_amount}-{self.max_amount}")
        setattr(obj, '_value', value)

    def __set_name__(self, owner, name) -> None:
        setattr(owner, name, self)


class Visitor:
    def __init__(self, name, age, weight, height) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age_range, weight_range, height_range) -> None:
        self.age_range = age_range
        self.weight_range = weight_range
        self.height_range = height_range

    def can_access(self, visitor) -> bool:
        return (
            self.age_range.min_amount <= visitor.age <= self.age_range.max_amount
            and self.weight_range.min_amount <= visitor.weight <= self.weight_range.max_amount
            and self.height_range.min_amount <= visitor.height <= self.height_range.max_amount
        )


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(IntegerRange(4, 14),
                         IntegerRange(20, 50),
                         IntegerRange(80, 120))


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(IntegerRange(14, 60),
                         IntegerRange(50, 120),
                         IntegerRange(120, 220))


class Slide:
    def __init__(self, name, limitation_class) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor) -> bool:
        return self.limitation_class.can_access(visitor)
