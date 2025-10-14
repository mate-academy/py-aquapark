from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner, name) -> None:
        self.protected_name = "_" + name

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"'{self.protected_name[1:]}' must be an integer.")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"'{self.protected_name[1:]}' must be between {self.min_amount} and {self.max_amount}.")
        instance.__dict__[self.protected_name] = value


    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.protected_name)


class Visitor:
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
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, weight: int, height: int):
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int, height: int):
        super().__init__(age, weight, height)


class Slide:
    def __init__(self, name: str, limitation_class: type):
        self.name= name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(age=visitor.age, weight=visitor.weight, height=visitor.height)
            return True
        except Exception:
            return False
