from abc import ABC
from typing import Any


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
        owner: type,
        name: str,
    ) -> None:
        self.name = f"_{name}"

    def __get__(
        self,
        instance: Any,
        owner: type,
    ) -> Any:
        if instance is None:
            return self

        return getattr(instance, self.name)

    def __set__(
        self,
        instance: Any,
        value: int,
    ) -> None:
        if not isinstance(value, int):
            raise TypeError

        if not self.min_amount <= value <= self.max_amount:
            raise ValueError

        setattr(instance, self.name, value)


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
    age = IntegerRange(0, 100)
    weight = IntegerRange(0, 300)
    height = IntegerRange(0, 300)

    def __init__(
        self,
        age: int,
        weight: int,
        height: int,
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(
    SlideLimitationValidator,
):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(
    SlideLimitationValidator,
):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)


class Slide:
    def __init__(
        self,
        name: str,
        limitation_class: type,
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(
        self,
        visitor: Visitor,
    ) -> bool:
        try:
            self.limitation_class(
                visitor.age,
                visitor.weight,
                visitor.height,
            )
        except (
            TypeError,
            ValueError,
        ):
            return False

        return True
