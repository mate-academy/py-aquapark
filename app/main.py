from abc import ABC
from typing import Type, Any


class IntegerRange:
    def __init__(
            self,
            min_amount: int,
            max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        if self.min_amount  < 0 or self.max_amount < 0:
            raise ValueError
        if self.min_amount > self.max_amount:
            raise ValueError

    def __set_name__(self, owner: Any, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> int:
        value = getattr(instance, self.protected_name)
        self.validate(value)
        return value

    def __set__(self, instance: Any, value: int) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)


    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        if value not in range(self.min_amount, self.max_amount + 1):
            raise ValueError


class Visitor:
   def __init__(
           self,
           name: str,
           age: int,
           weight: int,
           height: int
   ) -> None:
       self.name = name
       self.age = age
       self.weight = weight
       self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
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
    def __init__(
            self,
            name: str,
            limitation_class: Type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
        except (ValueError, TypeError):
            return False
        return True

visitor = Visitor(name="User", age=25, weight=135, height=160)
adult_slid = Slide(name="Adult Slide", limitation_class=AdultSlideLimitationValidator)
print(adult_slid.can_access(visitor))
print("#")