from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: any, owner: any) -> None:
        return getattr(instance, self._name)

    def __set__(self, instance: any, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"""{self._name} must be between
{self.min_amount} and {self.max_amount}""")
        return setattr(instance, self._name, value)

    def __set_name__(self, owner: any, name: str) -> None:
        self._name = "_" + name


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age_range: IntegerRange,
            weight_range: IntegerRange,
            height_range: IntegerRange
    ) -> None:
        self.age_range = age_range
        self.weight_range = weight_range
        self.height_range = height_range

    @abstractmethod
    def validate(self, visitor: Visitor) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age_range = IntegerRange(4, 14)
        height_range = IntegerRange(80, 120)
        weight_range = IntegerRange(20, 50)
        super().__init__(age_range, weight_range, height_range)

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age_range.min_amount
            <= visitor.age
            <= self.age_range.max_amount
            and self.height_range.min_amount
            <= visitor.height <= self.height_range.max_amount
            and self.weight_range.min_amount
            <= visitor.weight <= self.weight_range.max_amount
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age_range = IntegerRange(14, 60)
        height_range = IntegerRange(120, 220)
        weight_range = IntegerRange(50, 120)
        super().__init__(age_range, weight_range, height_range)

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age_range.min_amount
            <= visitor.age
            <= self.age_range.max_amount
            and self.height_range.min_amount
            <= visitor.height <= self.height_range.max_amount
            and self.weight_range.min_amount
            <= visitor.weight <= self.weight_range.max_amount
        )


class Slide:
    def __init__(self, name: str, limitation_class: any) -> None:
        self.age = None
        self.weight = None
        self.height = None
        self._name = name
        self.limitation_validator = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        self.age = visitor.age
        self.weight = visitor.weight
        self.height = visitor.height
        return self.limitation_validator.validate(visitor)
