from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.name = None
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object, owner: object) -> int:
        return instance.name

    def __set__(self, instance: object, value: int) -> None:
        instance.name = value

    def __set_name__(self, owner: object, name: str) -> None:
        self.name = name


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

    def validate(self, visitor: Visitor) -> bool:
        if (self.age.min_amount <= visitor.age <= self.age.max_amount
                and (self.weight.min_amount <= visitor.weight <= (
                    self.weight.max_amount))
                and (self.height.min_amount <= visitor.height <= (
                    self.height.max_amount))):
            return True
        return False


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            age=IntegerRange(4, 14),
            weight=IntegerRange(20, 50),
            height=IntegerRange(80, 120))


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            age=IntegerRange(14, 60),
            weight=IntegerRange(50, 120),
            height=IntegerRange(120, 220))


class Slide:
    def __init__(self, name: str, limitation_class: object) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.validate(visitor)
