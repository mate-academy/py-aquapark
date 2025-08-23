from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner, name) -> None:
        self.protected_name = '_' + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = getattr(obj, self.protected_name)
        return value

    def __set__(self, obj, value) -> None:
        if not isinstance(value, int):
            raise TypeError
        if not(self.min_amount <= value <= self.max_amount):
            raise ValueError
        setattr(obj, self.protected_name, value)


class Visitor:
   def __init__(self, name: str, age: int, weight: int | float, height: int | float) -> None:
       self.name = name
       self.age = age
       self.weight = weight
       self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int | float, height: int | float) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)
    def __init__(self, age: int, weight: int | float, height: int | float) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int | float, height: int | float) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class Slide:
    def __init__(self, name: str, limitation_class: ChildrenSlideLimitationValidator | AdultSlideLimitationValidator) -> None:
       self.name = name
       self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except(TypeError, ValueError):
            return False
