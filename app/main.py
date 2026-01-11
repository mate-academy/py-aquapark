from abc import ABC, abstractmethod
from typing import Type, Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        return getattr(obj, self.protected_name, None)

    def __set__(self, obj: Any, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"{self.protected_name} must be an integer.")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"{self.protected_name}"
                             f" should be between {self.min_amount}"
                             f" and {self.max_amount}.")
        setattr(obj, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.age = IntegerRange(4, 60)
        self.height = IntegerRange(80, 220)
        self.weight = IntegerRange(20, 120)

    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__()
        self.age = IntegerRange(4, 14)
        self.height = IntegerRange(80, 120)
        self.weight = IntegerRange(20, 50)

    def validate(self, visitor: Visitor) -> bool:
        if not (self.age.min_amount
                <= visitor.age <= self.age.max_amount):
            return False
        if not (self.height.min_amount
                <= visitor.height <= self.height.max_amount):
            return False
        if not (self.weight.min_amount
                <= visitor.weight <= self.weight.max_amount):
            return False
        return True


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__()
        self.age = IntegerRange(14, 60)
        self.height = IntegerRange(120, 220)
        self.weight = IntegerRange(50, 120)

    def validate(self, visitor: Visitor) -> bool:
        if not (self.age.min_amount
                <= visitor.age <= self.age.max_amount):
            return False
        if not (self.height.min_amount
                <= visitor.height <= self.height.max_amount):
            return False
        if not (self.weight.min_amount
                <= visitor.weight <= self.weight.max_amount):
            return False
        return True


class Slide:
    def __init__(self, name: str,
                 limitation_class: Type[SlideLimitationValidator]
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        validator = self.limitation_class()
        return validator.validate(visitor)
