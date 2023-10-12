from abc import ABC
from typing import Any


class IntegerRange:

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, value: str) -> None:
        self.protected_name = "_" + value

    def __get__(self, instance: Any, owner: Any) -> Any:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        setattr(instance, self.protected_name, value)


class Visitor:

    def __init__(self,
                 name: str,
                 age: int,
                 weight: int,
                 height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight

    def validate_visitor(self, visitor: Visitor) -> bool:
        if visitor.age not in range(self.age.min_amount,
                                    self.age.max_amount + 1):
            return False
        if visitor.height not in range(self.height.min_amount,
                                       self.height.max_amount + 1):
            return False
        if visitor.weight not in range(self.weight.min_amount,
                                       self.weight.max_amount + 1):
            return False
        return True


"""
    def validate_visitor(self, visitor: Visitor) -> Visitor:
        if visitor.age < self.age.min_amount:
            raise TypeError(f"{visitor.name} is too young for this slide.")
        if visitor.age > self.age.max_amount:
            raise TypeError(f"{visitor.name} is too old for this slide.")
        if visitor.height < self.height.min_amount:
            raise TypeError(f"{visitor.name} is too short for this slide.")
        if visitor.height > self.height.max_amount:
            raise TypeError(f"{visitor.name} is too tall for this slide.")
        if visitor.weight < self.weight.min_amount:
            raise TypeError(f"{visitor.name} weight "
                            "is too low for this slide.")
        if visitor.weight > self.weight.max_amount:
            raise TypeError(f"{visitor.name} weight is too "
                            "high for this slide.")
        return visitor
 """


class ChildrenSlideLimitationValidator(SlideLimitationValidator):

    def __init__(self) -> None:
        self.age = IntegerRange(4, 14)
        self.height = IntegerRange(80, 120)
        self.weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):

    def __init__(self) -> None:
        self.age = IntegerRange(14, 60)
        self.height = IntegerRange(120, 220)
        self.weight = IntegerRange(50, 120)


class Slide:

    def __init__(self,
                 name: str,
                 limitation_class : SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> Visitor:
        return self.limitation_class.validate_visitor(visitor)
