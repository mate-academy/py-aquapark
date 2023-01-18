from abc import ABC


class IntegerRange:

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: object, owner: object) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if isinstance(value, int) is False:
            raise TypeError(f"Wrong value type for {self.protected_name}."
                            f"It should be filled with an integer type value.")
        if self.max_amount < value or value < self.min_amount:
            raise ValueError(f"Wrong amount for{self.protected_name}."
                             f"It should be in range between"
                             f"{self.min_amount} and {self.max_amount}.")

        setattr(instance, self.protected_name, value)

    def validate(self, value: int) -> bool:
        if isinstance(value, int) is False:
            return False
        if self.max_amount < value or value < self.min_amount:
            return False
        return True


class Visitor:

    def __init__(
        self,
        name: str,
        age: int,
        height: int,
        weight: int
    ) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):

    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


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

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                visitor.age,
                visitor.height,
                visitor.weight
            )
        except ValueError or TypeError:
            return False
        return True
