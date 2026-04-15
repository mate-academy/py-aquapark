from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_amount = min_value
        self.max_amount = max_value

    def __set_name__(self, owner: Any, method_name: Any) -> None:
        self.protected_name = "_" + method_name

    def __get__(self, instance: Any, owner: Any) -> Any:
        value = getattr(instance, self.protected_name)
        return value

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.protected_name, value)
        else:
            raise ValueError


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
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(self, name: str, limitation_class: Any) -> None:
        self.name = name
        if not issubclass(limitation_class, SlideLimitationValidator):
            raise TypeError
        self.limitation_class = limitation_class

    def can_access(self, person: Visitor) -> bool:
        try:
            self.limitation_class(person.age, person.weight, person.height)
        except Exception:
            return False
        return True
