from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object, owner: type) -> str:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(f"{value} must be between "
                             f"{self.min_amount} and {self.max_amount}")
        setattr(instance, self.protected_name, value)

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name


class Visitor:
    def __init__(self,
                 name: str,
                 age: int,
                 weight: float,
                 height: float) -> None:
        self.name = name
        self.age = age
        self. weight = weight
        self. height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: float, height: float) -> None:
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
    def __init__(self,
                 name: str,
                 limitation_class: "SlideLimitationValidator") -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, instance: "Visitor") -> bool:
        try:
            self.limitation_class(
                instance.age, instance.weight, instance.height
            )
            return True
        except ValueError:
            return False
