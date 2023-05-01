from abc import ABC


class IntegerRange:
    def __init__(
            self,
            min_amount: int,
            max_amount: int
    ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: type) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> bool:
        if not (self.min_amount <= value <= self.max_amount):
            return False
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


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(self, name: str, limitation_class: object) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: type[Visitor]) -> bool:
        if issubclass(self.limitation_class, AdultSlideLimitationValidator):
            return (14 <= visitor.age <= 60
                    and 120 <= visitor.height <= 220
                    and 50 <= visitor.weight <= 120)
        if issubclass(self.limitation_class, ChildrenSlideLimitationValidator):
            return (4 <= visitor.age <= 14
                    and 80 <= visitor.height <= 120
                    and 20 <= visitor.weight <= 50)
