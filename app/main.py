from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount: int = min_amount
        self.max_amount: int = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name: str = "_" + name

    def __get__(self, instance: object, owner: type) -> int | None:
        return getattr(instance, self.protected_name, None)

    def __set__(self, instance: object, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"Value {value} is out of range "
                             f"({self.min_amount}-{self.max_amount})")
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name: str = name
        self.age: int = age
        self.weight: int = weight
        self.height: int = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age: int = age
        self.weight: int = weight
        self.height: int = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(
            self, name: str, limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name: str = name
        self.limitation_class: type[SlideLimitationValidator]
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                visitor.age, visitor.weight, visitor.height
            )
            return True
        except ValueError as e:
            print(f"Access denied: {e}")
            return False
