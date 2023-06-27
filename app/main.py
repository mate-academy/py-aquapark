from abc import ABC, abstractmethod
from typing import Type


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
    @abstractmethod
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = weight

    @abstractmethod
    def get_access(self) -> bool:
        pass


class IntegerRange:

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.status_access = None

    def __set_name__(self,
                     owner: Type[SlideLimitationValidator],
                     name: str) -> None:
        self.status_access = "_" + name

    def __get__(self,
                instance: Type[SlideLimitationValidator],
                owner: Type[SlideLimitationValidator]
                ) -> bool:
        return getattr(instance, self.status_access)

    def __set__(self,
                instance: Type[SlideLimitationValidator],
                value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(
                f"{self.status_access} should be integer,"
                f" not a {type(value)}!"
            )
        setattr(
            instance,
            self.status_access,
            self.min_amount <= value <= self.max_amount
        )


class ChildrenSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    def get_access(self) -> bool:
        return all([self.age, self.weight, self.height])


class AdultSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    def get_access(self) -> bool:
        return all([self.age, self.weight, self.height])


class Slide:

    def __init__(
            self,
            name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Type[Visitor]) -> bool:
        return self.limitation_class(
            age=visitor.age,
            weight=visitor.weight,
            height=visitor.height
        ).get_access()
