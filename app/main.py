from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object, owner: type) -> int:
        return getattr(instance, self.name)

    def __set__(self, instance: object, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"Value must be between"
                f" {self.min_amount} and {self.max_amount}"
            )
        setattr(instance, self.name, value)


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age = IntegerRange(4, 14)
        height = IntegerRange(80, 120)
        weight = IntegerRange(20, 50)
        super().__init__(age, height, weight)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age = IntegerRange(14, 60)
        height = IntegerRange(120, 220)
        weight = IntegerRange(50, 120)
        super().__init__(age, height, weight)


class Visitor:
    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_validator = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return (self.limitation_validator.age.min_amount <= visitor.age
                <= self.limitation_validator.age.max_amount
                and self.limitation_validator.weight.min_amount
                <= visitor.weight
                <= self.limitation_validator.weight.max_amount
                and self.limitation_validator.height.min_amount
                <= visitor.height
                <= self.limitation_validator.height.max_amount
                )
