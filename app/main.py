from abc import ABC


class IntegerRange:

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner, name) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance, owner) -> "IntegerRange":
        return getattr(instance, self.protected_name)

    def __set__(self, instance, value: int | float) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Expected int, got {type(value)}")
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.protected_name, value)
        else:
            raise ValueError(f"Value {value} is out of range")


class Visitor:

    def __init__(self, name: str, age: int,
                 weight: int | float, height: int | float) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):

    def __init__(self, age: int,
                 weight: int | float, height: int | float) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def __init__(self, age: int,
                 weight: int | float, height: int | float) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def __init__(self, age: int, weight: int | float,
                 height: int | float) -> None:
        super().__init__(age, weight, height)


class Slide:

    def __init__(self, name: str,
                 limitation_class: "ChildrenSlideLimitationValidator" or "AdultSlideLimitationValidator") -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except (ValueError, TypeError):
            return False
