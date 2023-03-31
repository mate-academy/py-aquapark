from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: int, name: str) -> str:
        pass

    def __get__(self, instance: int, owner: str) -> None:
        pass

    def __set__(self, instance: str, value: int) -> str:
        pass


class Visitor:
    def __init__(
            self, age: int, height: int, weight: int, name: str = ""
    ) -> None:
        self.age = age
        self.height = height
        self.weight = weight
        self.name = name


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight

    def has_access(self, value: int) -> str:
        if self.min_amount <= value <= self.max_amount:
            has_access = True
        param = (self.age, self.height, self.weight, {has_access}, {id})
        return param


class ChildrenSlideLimitationValidator(SlideLimitationValidator, IntegerRange):
    age = IntegerRange(min_amount=4, max_amount=14)
    height = IntegerRange(min_amount=80, max_amount=120)
    weight = IntegerRange(min_amount=20, max_amount=50)

    def get(self) -> bool:
        if (
            not (4 <= self.age <= 14)
            or not (80 <= self.height <= 120)
            or not (20 <= self.weight <= 50)
        ):
            return False
        else:
            return True


class AdultSlideLimitationValidator(SlideLimitationValidator, IntegerRange):
    age = IntegerRange(min_amount=14, max_amount=60)
    height = IntegerRange(min_amount=120, max_amount=220)
    weight = IntegerRange(min_amount=50, max_amount=120)

    def get(self) -> bool:
        if (
            not (14 <= self.age <= 60)
            or not (120 <= self.height <= 220)
            or not (50 <= self.weight <= 120)
        ):
            return False
        else:
            return True


class Slide:
    def __init__(self, name: str, limitation_class: int) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        self.age = visitor.age
        self.height = visitor.height
        self.weight = visitor.weight
        if self.limitation_class == AdultSlideLimitationValidator:
            return AdultSlideLimitationValidator.get(self)
        elif self.limitation_class == ChildrenSlideLimitationValidator:
            return ChildrenSlideLimitationValidator.get(self)
