from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner: classmethod, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self,
                instance: classmethod,
                owner: int | float) -> int | float:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: classmethod, value: int | float) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        if not self.min_value <= value <= self.max_value:
            raise ValueError(f"Value must be between "
                             f"{self.min_value} and {self.max_value}")
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    @abstractmethod
    def __init__(self, name: str, weight: int, height: int) -> None:
        self.name = name
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class Slide:
    def __init__(self, name: str, limitation_class: classmethod) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
        except (TypeError, ValueError):
            return False
        else:
            return True
