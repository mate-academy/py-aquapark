from abc import ABC


class IntegerRange:
    """Data validation descriptor"""

    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, instance: type, name: str) -> None:
        self.private_name = f"_{name}"

    def __get__(self, instance: type, owner: type) -> str:
        return getattr(instance, self.private_name)

    def __set__(self, instance: type, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"{self.private_name} must be integer!")
        if not self.min_value <= value <= self.max_value:
            raise ValueError(f"Value must be in range from "
                             f"{self.min_value} to {self.max_value}")
        setattr(instance, self.private_name, value)


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
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
        except (ValueError, TypeError):
            return False
        return True
