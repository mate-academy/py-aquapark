from abc import ABC


class IntegerRange:
    def __init__(self,
                 min_amount: int,
                 max_amount: int
                 ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: object, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, instance: object, owner: type) -> int:
        value = getattr(instance, self.private_name)
        return value

    def __set__(self, instance: object, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"Value should be within range: "
                             f"{self.min_amount} - {self.max_amount}.")
        setattr(instance, self.private_name, value)


class Visitor:
    def __init__(self,
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

    def __init__(self,
                 age: int,
                 height: int,
                 weight: int
                 ) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age_range = IntegerRange(4, 14)
    height_range = IntegerRange(80, 120)
    weight_range = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age_range = IntegerRange(14, 60)
    height_range = IntegerRange(120, 220)
    weight_range = IntegerRange(50, 120)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: type(SlideLimitationValidator)
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        validator = self.limitation_class(visitor.age, visitor.weight, visitor.height)
        return (
                validator.age.min_amount <= visitor.age <= validator.age.max_amount
                and validator.height.min_amount <= visitor.height <= validator.height_range.max_amount
                and validator.weight_range.min_amount <= visitor.weight <= validator.weight_range.max_amount
        )
