from abc import ABC, abstractmethod
from typing import Any, Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Type[Any], name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, obj: Any, objtype: Type[Any] = None) -> Any:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: Any, value: int) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(obj, self.protected_name, value)


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

    @abstractmethod
    def validate(self) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def validate(self) -> bool:
        return (4 <= self.age <= 14
                and 80 <= self.height <= 120
                and 20 <= self.weight <= 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def validate(self) -> bool:
        return (14 <= self.age <= 60
                and 120 <= self.height <= 220
                and 50 <= self.weight <= 120)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        result = self.limitation_class(
            age=visitor.age,
            height=visitor.height,
            weight=visitor.weight
        ).validate()
        return result
