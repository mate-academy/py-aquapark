from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner, name: str) -> None:
        self.private_name = "_" + name
        print(f"__set_name__ called: {self.private_name}")

    def __get__(self, obj, objtype=None) -> int:
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"{value} is out of range "
                             f"({self.min_amount}, {self.max_amount})")
        setattr(obj, self.private_name, value)


class Visitor:
    def __init__(self,
                 name: str,
                 age: int,
                 weight: int,
                 height: int
                 ) -> None:
        self.name = name
        self.weight = weight
        self.height = height
        self.age = age


class SlideLimitationValidator(ABC):
    @staticmethod
    @abstractmethod
    def validate(visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    @staticmethod
    def validate(visitor: Visitor) -> bool:
        return (4 <= visitor.age <= 14
                and 20 <= visitor.weight <= 50
                and 80 <= visitor.height <= 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    @staticmethod
    def validate(visitor: Visitor) -> bool:
        return (14 <= visitor.age <= 60
                and 50 <= visitor.weight <= 120
                and 120 <= visitor.height <= 220)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: SlideLimitationValidator
                 ) -> None:
        self.name = name
        self.limitation_validator = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_validator.validate(visitor)
