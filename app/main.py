from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object, owner: type) -> int:
        return instance.__dict__[self.name]

    def __set__(self, instance: object, value: int) -> None:
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"{self.name} should be between {self.min_amount}"
                f" and {self.max_amount}"
            )
        instance.__dict__[self.name] = value


class Visitor:
    age = IntegerRange(0, 120)
    weight = IntegerRange(0, 300)
    height = IntegerRange(0, 250)

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def validate(self, visitor: Visitor) -> bool:
        return (
            4 <= visitor.age <= 13
            and 20 <= visitor.weight <= 49
            and 80 <= visitor.height <= 119
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def validate(self, visitor: Visitor) -> bool:
        return (
            14 <= visitor.age <= 60
            and 50 <= visitor.weight <= 120
            and 120 <= visitor.height <= 220
        )


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.validate(visitor)
