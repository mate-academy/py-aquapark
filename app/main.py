from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = "_" + name

    def __get__(self, instance: object, owner: type) -> int:
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("It's not integer")
        if value < self.min_amount or value > self.max_amount:
            raise ValueError("The integer must be in limit")
        instance.__dict__[self.name] = value


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
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)


class Slide:
    def __init__(self, name: str,
                 limitation_class: "SlideLimitationValidator") -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: "Visitor") -> bool:
        try:
            self.limitation_class.age.__set__(visitor, visitor.age)
            self.limitation_class.weight.__set__(visitor, visitor.weight)
            self.limitation_class.height.__set__(visitor, visitor.height)
            return True
        except (TypeError, ValueError):
            return False
