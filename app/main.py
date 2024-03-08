from abc import ABC
from typing import Type, Any


class IntegerRange:
    def __init__(self,
                 min_amount: int,
                 max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Value should be an integer")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"Value should not be less than {self.min_amount} "
                f"and greater than {self.max_amount} "
            )
        return setattr(instance, self.protected_name, value)


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
    def __init__(self,
                 name: str,
                 age: int,
                 weight: int,
                 height: int
                 ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(min_amount=4, max_amount=14)
    height = IntegerRange(min_amount=80, max_amount=120)
    weight = IntegerRange(min_amount=20, max_amount=50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(min_amount=14, max_amount=60)
    height = IntegerRange(min_amount=120, max_amount=220)
    weight = IntegerRange(min_amount=50, max_amount=120)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: Type[SlideLimitationValidator]) -> None:
        self.name = name
        self.imitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.imitation_class(
                name=visitor.name,
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height
            )
        except ValueError:
            return False

        return True
