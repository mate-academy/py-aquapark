from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: int, owner: int) -> None:
        return getattr(instance, self.name)

    def __set__(self, instance: int, value: int) -> None:
        if value < self.min_amount or value > self.max_amount:
            raise ValueError(f"{self.name} must be between "
                             f"{self.min_amount} and {self.max_amount}")
        setattr(instance, self.name, value)

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
        self.age = age
        self.weight = weight
        self.height = height

    def is_valid(self, visitor: Visitor) -> bool:
        value = [
            self.age.min_amount <= visitor.age,
            visitor.age <= self.age.max_amount,
            self.weight.min_amount <= visitor.weight,
            visitor.weight <= self.weight.max_amount,
            self.height.min_amount <= visitor.height,
            visitor.height <= self.height.max_amount
        ]
        return all(value)


class ChildrenSlideLimitationValidator(SlideLimitationValidator):

    def __init__(self) -> None:
        super().__init__(
            age=IntegerRange(4, 14),
            weight=IntegerRange(20, 50),
            height=IntegerRange(80, 120)
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):

    def __init__(self) -> None:
        super().__init__(
            age=IntegerRange(14, 60),
            weight=IntegerRange(50, 120),
            height=IntegerRange(120, 220)
        )


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_validator = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_validator.is_valid(visitor)
