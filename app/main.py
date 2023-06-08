from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.max_amount = max_amount
        self.min_amount = min_amount

    def __set_name__(self, owner: any, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: any, owner: any) -> any:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: any, value: any) -> any:
        if value < self.min_amount or value > self.max_amount:
            raise ValueError("Value out of range")
        if type(value) != int:
            raise TypeError("Value must be int")
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.height = height
        self.weight = weight
        self.age = age
        self.name = name


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.height = height
        self.weight = weight
        self.age = age


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(self, name: str,
                 limitation_class: SlideLimitationValidator) -> None:
        self.limitation_class = limitation_class
        self.name = name

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age,
                                  visitor.weight,
                                  visitor.height)
        except ValueError:
            return False
        return True
