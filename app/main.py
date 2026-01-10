from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.protected_name = None

    def __get__(self, instance: object, owner: object) -> object:
        return getattr(instance, self.protected_name)

    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = "_" + name

    def __set__(self, instance: object, value: str) -> None:
        setattr(instance, self.protected_name, value)


class Visitor:
    age = IntegerRange(0, 0)
    height = IntegerRange(0, 0)
    weight = IntegerRange(0, 0)

    def __init__(self, name: str, age: str,
                 weight: str, height: str) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int,
                 weight: int,
                 height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age=IntegerRange(4, 14),
                         weight=IntegerRange(20, 50),
                         height=IntegerRange(80, 120))

    def can_use_slide(self, visitor: object) -> None:
        return ((4 <= visitor.age <= 14)
                and (80 <= visitor.height <= 120)
                and (20 <= visitor.weight <= 50))


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age=IntegerRange(14, 60),
                         weight=IntegerRange(50, 120),
                         height=IntegerRange(120, 220))

    def can_use_slide(self, visitor: object) -> bool:
        return ((14 <= visitor.age <= 60)
                and (120 <= visitor.height <= 220)
                and (50 <= visitor.weight <= 120))


class Slide:
    def __init__(self, name: str, limitation_class: object) -> None:
        self.name = name
        self.limitation_validator = limitation_class()

    def can_access(self, visitor: object) -> bool:
        return self.limitation_validator.can_use_slide(visitor)
