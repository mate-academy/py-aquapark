from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object, owner: type[object]) -> int:
        return instance.__dict__[self.name]

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("Value must be an integer.")
        if value < self.min_amount or value > self.max_amount:
            raise ValueError(
                f"Value must be between {self.min_amount}"
                f" and {self.max_amount}."
            )
        instance.__dict__[self.name] = value

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.name = name


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height

        self.age_range = IntegerRange(0, 150)
        self.weight_range = IntegerRange(0, 500)
        self.height_range = IntegerRange(0, 300)


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
    def validate(self, visitor: type[Visitor]) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age_range = IntegerRange(4, 14)
        height_range = IntegerRange(80, 120)
        weight_range = IntegerRange(20, 50)
        super().__init__(age_range, weight_range, height_range)

    def validate(self, visitor: type[Visitor]) -> bool:
        if self.age_range.min_amount <= \
                visitor.age <= self.age_range.max_amount and \
           self.height_range.min_amount <= \
                visitor.height <= self.height_range.max_amount and \
           self.weight_range.min_amount <= \
                visitor.weight <= self.weight_range.max_amount:
            return True
        return False


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age_range = IntegerRange(14, 60)
        height_range = IntegerRange(120, 220)
        weight_range = IntegerRange(50, 120)
        super().__init__(age_range, weight_range, height_range)

    def validate(self, visitor: type[Visitor]) -> bool:
        if self.age_range.min_amount <=\
                visitor.age <= self.age_range.max_amount and \
           self.height_range.min_amount <= \
                visitor.height <= self.height_range.max_amount and \
           self.weight_range.min_amount <= \
                visitor.weight <= self.weight_range.max_amount:
            return True
        return False


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_validator = limitation_class()

    def can_access(self, visitor: type[Visitor]) -> bool:
        return self.limitation_validator.validate(visitor)
