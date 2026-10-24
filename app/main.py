from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: object) -> int | float:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> int | float:
        if not isinstance(value, (int, float)):
            raise TypeError()
        if value > self.max_amount or value < self.min_amount:
            raise ValueError()
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int,
                 weight: float, height: float) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, height: float, weight: float) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, height: float, weight: float) -> None:
        super().__init__(age, height, weight)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, height: float, weight: float) -> None:
        super().__init__(age, height, weight)


class Slide:
    def __init__(self, name: str,
                 limitation_class: type[SlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: type[Visitor]) -> bool:
        try:
            self.limitation_class(
                age=visitor.age,
                height=visitor.height,
                weight=visitor.weight
            )
            return True
        except (TypeError, ValueError):
            return False
