from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: any, owner: any) -> any:
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance: any, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"Value must be between {self.min_amount} "
                             f"and {self.max_amount}")
        instance.__dict__[self.name] = value

    def __set_name__(self, owner: any, name: str) -> None:
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
            age_range: int,
            weight_range: int,
            height_range: int
    ) -> None:
        self.age_range = age_range
        self.weight_range = weight_range
        self.height_range = height_range

    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        self.age_range = IntegerRange(4, 14)
        self.height_range = IntegerRange(80, 120)
        self.weight_range = IntegerRange(20, 50)

    def validate(self, visitor: Visitor) -> bool:
        return all([
            self.age_range.min_amount <= visitor.age
            <= self.age_range.max_amount,

            self.height_range.min_amount <= visitor.height
            <= self.height_range.max_amount,

            self.weight_range.min_amount <= visitor.weight
            <= self.weight_range.max_amount
        ])


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        self.age_range = IntegerRange(14, 60)
        self.height_range = IntegerRange(120, 220)
        self.weight_range = IntegerRange(50, 120)

    def validate(self, visitor: Visitor) -> bool:
        return all([
            self.age_range.min_amount <= visitor.age
            <= self.age_range.max_amount,

            self.height_range.min_amount <= visitor.height
            <= self.height_range.max_amount,

            self.weight_range.min_amount <= visitor.weight
            <= self.weight_range.max_amount
        ])


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.validate(visitor)
