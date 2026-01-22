from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner, name):
        self.public_name = "_" + name

    def __get__(self, instance: object, owner):
        return getattr(instance, self.public_name)

    def __set__(self, instance: object, value):
        if type(value) is not int:
            raise TypeError
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.public_name, value)
        else:
            raise ValueError("ERROR")


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
    def __init__(self, name: str, limitation_class) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor):
        try:
            person = self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except TypeError:
            return False
        except ValueError:
            return False
