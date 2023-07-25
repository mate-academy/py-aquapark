from abc import ABC, abstractmethod
from typing import Tuple


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: None, owner: None) -> str:
        return getattr(instance, self.name)

    def __set__(self, instance: None, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("Value must be an integer.")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError((f"Value must be in the range"
                              f" [{self.min_amount}, {self.max_amount}]."))
        setattr(instance, self.name, value)

    def __set_name__(self, owner: None, name: str) -> None:
        self.name = name


class Visitor:
    age = IntegerRange(0, 150)
    weight = IntegerRange(0, 500)
    height = IntegerRange(0, 300)

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age_range: Tuple[int, int],
            height_range: Tuple[int, int],
            weight_range: Tuple[int, int]
    ) -> None:
        self.age_range = IntegerRange(*age_range)
        self.height_range = IntegerRange(*height_range)
        self.weight_range = IntegerRange(*weight_range)

    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator, ABC):
    age_range = (4, 14)
    height_range = (80, 120)
    weight_range = (20, 50)

    def __init__(self) -> None:
        super().__init__(self.age_range, self.height_range, self.weight_range)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        age_range = (14, 60)
        height_range = (120, 220)
        weight_range = (50, 120)
        super().__init__(age_range, height_range, weight_range)


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        limitation_validator = self.limitation_class()
        return limitation_validator.validate(visitor)
