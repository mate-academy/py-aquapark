from abc import ABC
from typing import Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.protected_name = ""

    def __set_name__(self, owner: Type, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: object, owner: Type) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"{self.protected_name[1:]} should be an integer.")
        if value < self.min_amount or value > self.max_amount:
            raise ValueError(f"{self.protected_name[1:]} "
                             f"should be between {self.min_amount} "
                             f"and {self.max_amount}.")
        setattr(instance, self.protected_name, value)


class Visitor:
    age: IntegerRange
    weight: IntegerRange
    height: IntegerRange

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self._age = age
        self._weight = weight
        self._height = height

    age = IntegerRange(0, 120)
    weight = IntegerRange(1, 500)
    height = IntegerRange(30, 300)

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        IntegerRange(0, 120).__set__(self, value)

    @property
    def weight(self) -> int:
        return self._weight

    @weight.setter
    def weight(self, value: int) -> None:
        IntegerRange(1, 500).__set__(self, value)

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        IntegerRange(30, 300).__set__(self, value)


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age: IntegerRange,
                 weight: IntegerRange,
                 height: IntegerRange) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age = IntegerRange(4, 14)
        weight = IntegerRange(20, 50)
        height = IntegerRange(80, 120)
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age = IntegerRange(14, 60)
        weight = IntegerRange(50, 120)
        height = IntegerRange(120, 220)
        super().__init__(age, weight, height)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: Type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            limitation = self.limitation_class()
            limitation.age.__set__(visitor, visitor.age)
            limitation.weight.__set__(visitor, visitor.weight)
            limitation.height.__set__(visitor, visitor.height)
            return True
        except (TypeError, ValueError) as e:
            print(f"Access Denied: {e}")
            return False
