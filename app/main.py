from __future__ import annotations
from abc import ABC


class IntegerRange:
    def __init__(
            self,
            min_value: int,
            max_value: int
    ) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(
            self,
            owner: SlideLimitationValidator,
            name: str
    ) -> None:
        self.protected_name = "_" + name

    def __get__(
            self,
            instance: IntegerRange,
            owner: SlideLimitationValidator
    ) -> int:
        return getattr(instance, self.protected_name)

    def __set__(
            self,
            instance: IntegerRange,
            value: int
    ) -> None:
        if value not in range(self.min_value, self.max_value + 1):
            raise ValueError(
                f"parameter: {self.protected_name} = {value}"
                f" out of acceptable range:"
                f" {self.min_value} - {self.max_value}"
            )
        setattr(instance, self.protected_name, value)


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
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                visitor.age,
                visitor.weight,
                visitor.height
            )
        except ValueError as e:
            print(f"visitor: {visitor.name} ", e)
            return False
        return True
