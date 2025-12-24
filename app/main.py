from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(
            self,
            min_amount: int,
            max_amount: int
    ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(
            self,
            obj: Any,
            objtype: None | Any = None
    ) -> int | str:
        value = getattr(obj, self.private_name, None)
        return value

    def __set__(
            self,
            obj: Any,
            value: int
    ) -> None:
        if not isinstance(value, int):
            raise TypeError(f"{value} must be an integer")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"{value} must be between "
                f"{self.min_amount} and {self.max_amount}"
            )
        setattr(obj, self.private_name, value)

    def __set_name__(
            self,
            owner: Any,
            name: str
    ) -> None:
        self.public_name = name
        self.private_name = "_" + name


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
    age = IntegerRange(4, 60)
    weight = IntegerRange(20, 120)
    height = IntegerRange(80, 120)

    def __init__(
            self,
            age: int,
            height: int,
            weight: int
    ) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def __init__(
            self,
            age: int,
            height: int,
            weight: int
    ) -> None:
        super().__init__(age, height, weight)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def __init__(
            self,
            age: int,
            height: int,
            weight: int
    ) -> None:
        super().__init__(age, height, weight)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: Any
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(
            self,
            visitor: Any
    ) -> bool:
        try:
            self.limitation_class(
                age=visitor.age,
                height=visitor.height,
                weight=visitor.weight
            )
            return True
        except ValueError:
            return False
