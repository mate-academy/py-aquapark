from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        # self.protected_name = None

    def __set_name__(self, owner: None, name: str) -> None:
        self.protected_name = f"_{name}"
        self.public_name = name

    def __get__(self, instance: None, owner: None) -> None:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: None, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Value {value} is not an integer")

        if not self.max_amount >= value >= self.min_amount:
            raise ValueError(f"Invalid value {value} for {self.public_name}")
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: int, age: int, weight: int, height: int) -> None:
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
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(self, name: str, limitation_class: None) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height
            )
            return True
        except (TypeError, ValueError):
            return False
