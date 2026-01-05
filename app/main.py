from abc import ABC
from typing import Type


class IntegerRange:
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(
            self,
            owner: "SlideLimitationValidator",
            name: str
    ) -> None:
        self.private_name = "_" + name

    def __get__(
            self,
            instance: "SlideLimitationValidator",
            owner: "SlideLimitationValidator"
    ) -> int:
        return getattr(instance, self.private_name)

    def __set__(
            self,
            instance: "SlideLimitationValidator",
            value: int
    ) -> None:
        if not isinstance(value, int):
            raise TypeError()
        if value < self.min_value or value > self.max_value:
            raise ValueError()
        setattr(instance, self.private_name, value)


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            height: int,
            weight: int
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, height: int, weight: int) -> None:
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
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.height, visitor.weight)
        except ValueError:
            return False
        except TypeError:
            return False
        return True
