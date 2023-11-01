from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: int, owner: int) -> None:
        return instance.__dict__[self.name]

    def __set__(self, instance: int, value: int) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.name, value)
        else:
            raise ValueError(
                f"{self.name} should be between "
                f"{self.min_amount} and {self.max_amount}"
            )

    def __set_name__(self, owner: int, name: int) -> None:
        self.name = f"_{name}"


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height

    age = IntegerRange(0, 150)
    weight = IntegerRange(0, 500)
    height = IntegerRange(0, 300)


class SlideLimitationValidator(ABC):
    def can_access(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def can_access(self, visitor: Visitor) -> bool:
        return 4 <= visitor.age <= 14 \
            and 80 <= visitor.height <= 120 \
            and 20 <= visitor.weight <= 50


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def can_access(self, visitor: Visitor) -> bool:
        return 14 <= visitor.age <= 60 \
            and 120 <= visitor.height <= 220 \
            and 50 <= visitor.weight <= 120


class Slide:
    def __init__(
            self, name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class().can_access(visitor)
