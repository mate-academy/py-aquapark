from abc import ABC, abstractmethod
from typing import Union


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, obj: object, objtype: object = None) -> object:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: object, value: object) -> None:
        self.validate(value)
        setattr(obj, self.protected_name, value)

    def validate(self, value: object) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")

        if value < self.min_amount or value > self.max_amount:
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_amount} and greater than "
                             f"{self.max_amount}.")


class Visitor:
    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    @abstractmethod
    def __init__(self, age: int, height: int, weight: int) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: Union[
                     ChildrenSlideLimitationValidator,
                     AdultSlideLimitationValidator
                 ]) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                visitor.age,
                visitor.height,
                visitor.weight
            )

        except ValueError:
            return False

        return True

# v = Visitor("Visitor", 17, 175, 67)

# slide1 = Slide("Slide1", ChildrenSlideLimitationValidator)

# print("1")
# print(slide1.can_access(v))
