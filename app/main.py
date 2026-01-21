from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int | float,
                 max_amount: int | float) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: type) -> int | str:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int | float) -> None:
        if isinstance(value, (int, float)):
            if self.min_amount <= value <= self.max_amount:
                setattr(instance, self.protected_name, value)
            else:
                raise ValueError(f"value must be in range of "
                                 f"{self.min_amount} to {self.max_amount}")
        else:
            raise TypeError("value must be int or float")


class Visitor:
    def __init__(self, name: str,
                 age: int, weight: int | float,
                 height: int | float) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int,
                 weight: int | float,
                 height: int | float) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except (ValueError, TypeError):
            return False
