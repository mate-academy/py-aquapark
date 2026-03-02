from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.value = None

    def __get__(self, instance: object, owner: type) -> int:
        return self.value

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer.")
        if value < self.min_amount or value > self.max_amount:
            raise ValueError(f"Value must be between "
                             f"{self.min_amount} and {self.max_amount}.")
        self.value = value

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name


class Visitor:
    age = IntegerRange(0, 120)
    weight = IntegerRange(0, 300)
    height = IntegerRange(0, 300)

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                visitor.age, visitor.weight, visitor.height)
            return True
        except (TypeError, ValueError):
            return False
