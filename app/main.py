from abc import ABC
from typing import Any, Type


class IntegerRange:
    def __init__(
            self,
            min_amount: int,
            max_amount: int,
    ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(
            self,
            owner: Any,
            name: str
    ) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(
            self,
            obj: Any,
            obj_type: Any = None
    ) -> Any:
        value = getattr(obj, self.protected_name)

        return value

    def __set__(
            self,
            obj: Any,
            value: int
    ) -> None:
        setattr(obj, self.protected_name, self.validate(value))

    def validate(self, value: int) -> int:
        if type(value) != int:
            raise TypeError(
                f"{self.public_name} should be integer."
            )

        if value < self.min_amount or value > self.max_amount:
            raise ValueError(
                f"{self.public_name} should not be less than "
                f"{self.min_amount} and greater than {self.max_amount}"
            )

        return value


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            weight: int,
            height: int,
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
            height: int,
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
            limitation_class: Type[SlideLimitationValidator],
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

            return True
        except ValueError:
            return False
