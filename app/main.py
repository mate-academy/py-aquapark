from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: "Slide", name: str) -> None:
        self.name = "_" + name

    def __get__(self, instance: "Slide", owner: "Slide") -> None:
        return getattr(instance, self.name)

    def __set__(self, instance: "Slide", value: int | str) -> None:
        if not isinstance(value, int):
            raise TypeError("Expected an integer")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(f"Expected an integer between "
                             f"{self.min_amount} and "
                             f"{self.max_amount}")
        setattr(instance, self.name, value)


class Visitor:
    def __init__(self, name: str,
                 age: int, weight: int | float,
                 height: int | float) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):

    def __init__(self, age: int,
                 weight: int | float,
                 height: int | float) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(self, name: str, limitation_class: object) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: "Visitor") -> bool:
        try:
            validator = self.limitation_class(visitor.age,
                                              visitor.weight,
                                              visitor.height)
            validator.age = visitor.age
            validator.height = visitor.height
            validator.weight = visitor.weight
            return True
        except (ValueError, TypeError):
            return False
