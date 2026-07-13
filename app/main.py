from abc import ABC
from typing import Any, Union, Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_value = min_amount
        self.max_value = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.name = name

    def __set__(self, instance: Any, value: Union[int, float]) -> None:
        if not isinstance(value, (int)):
            raise TypeError
        if value < self.min_value or value > self.max_value:
            raise ValueError
        else:
            instance.__dict__[self.name] = value

    def __get__(self, instance: Any, owner: Any) -> Union[int, float]:
        if instance is None:
            return self
        return instance.__dict__[self.name]


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
    def __init__(
            self,
            name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height
            )
        except (ValueError, TypeError):
            return False
        return True
