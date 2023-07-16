from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance, owner):
        pass

    def __set__(self, instance, value):
        pass

    def __set_name__(self, owner, name):
        pass


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


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)
        if 4 <= age <= 14:
            self.age = age
        if 80 <= weight <= 120:
            self.weight = weight
        if 20 <= height <= 50:
            self.height = height


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)
        if 14 <= age <= 60:
            self.age = age
        if 120 <= weight <= 220:
            self.weight = weight
        if 50 <= height <= 120:
            self.height = height


class Slide:
    def __init__(self, name: str, limitation_class: SlideLimitationValidator) -> None:
        pass


def can_access(visitor: Visitor) -> bool:
    return True
