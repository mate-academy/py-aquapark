from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object, owner: type) -> int:
        return instance.__dict__[self.name]

    def __set__(self, instance: object, value: int) -> None:
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(f"{self.name} out of range")
        instance.__dict__[self.name] = value

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name


class Visitor:
    age = IntegerRange(0, 150)
    height = IntegerRange(0, 300)
    weight = IntegerRange(0, 300)

    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight

    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def validate(self, visitor: Visitor) -> bool:
        return 4 <= visitor.age <= 14 \
            and 80 <= visitor.height <= 120 \
            and 20 <= visitor.weight <= 50


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def validate(self, visitor: Visitor) -> bool:
        return 14 <= visitor.age <= 60 \
            and 120 <= visitor.height <= 220 \
            and 50 <= visitor.weight <= 120


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: "SlideLimitationValidator"
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        limitation_validator = self.limitation_class(
            visitor.age,
            visitor.height,
            visitor.weight
        )
        return limitation_validator.validate(visitor)
