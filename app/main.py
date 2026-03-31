from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int,
                 max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: object, name: str) -> None:
        self.private_name = "_" + name
        self.public_name = name

    def __get__(self, instance: object, owner: object) -> int | float:
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: int | float) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.private_name, value)
        else:
            raise ValueError(f"{self.public_name} should be in range "
                             f"{self.min_amount}...{self.max_amount}")


class Visitor:
    def __init__(
            self, name: str, age: int,
            weight: int | float, height: int | float
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int | float,
                 height: int | float) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, weight: int | float,
                 height: int | float) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int | float,
                 height: int | float) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class Slide:
    def __init__(self, name: str,
                 limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:

        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
        except ValueError:
            return False
        else:
            return True
