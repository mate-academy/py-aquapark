from abc import ABC, abstractmethod
from typing import Any, Union


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(
            self,
            owner: Union[
                "ChildrenSlideLimitationValidator",
                "AdultSlideLimitationValidator"
            ],
            name: str
    ) -> None:
        self.protected_name = f"_{name}"

    def __get__(
            self,
            instance: Union[
                "ChildrenSlideLimitationValidator",
                "AdultSlideLimitationValidator"
            ],
            owner: Any
    ) -> bool:
        return getattr(instance, self.protected_name)

    def __set__(
            self,
            instance: Union[
                "ChildrenSlideLimitationValidator",
                "AdultSlideLimitationValidator"
            ],
            value: int
    ) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            value = False
        else:
            value = True

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

    @abstractmethod
    def validate(self) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def validate(self) -> bool:
        return self.age and self.height and self.weight


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 64)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def validate(self) -> bool:
        return self.age and self.height and self.weight


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: Union[
                "ChildrenSlideLimitationValidator",
                "AdultSlideLimitationValidator"
            ]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: "Visitor") -> bool:
        return self.limitation_class(
            age=visitor.age, weight=visitor.weight, height=visitor.height
        ).validate()
