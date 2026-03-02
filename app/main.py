from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: str, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: str, owner: str) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: str, value: str) -> None:
        if not isinstance(value, int):
            raise TypeError("Must be an integer")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"Value should be between"
                f" {self.min_amount} and {self.max_amount}."
            )

        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):

    age = IntegerRange(0, 0)
    weight = IntegerRange(0, 0)
    height = IntegerRange(0, 0)

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: list) -> bool:
        try:
            self.limitation_class(
                visitor.age,
                visitor.weight,
                visitor.height
            )
            return True
        except (TypeError, ValueError):
            return False
