from abc import ABC


class IntegerRange:
    def __init__(self, minvalue: int, maxvalue: int) -> None:
        self.min_value = minvalue
        self.max_value = maxvalue

    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: object) -> object:
        if instance is None:
            return self
        return getattr(instance, self.protected_name, 0)

    def __set__(self, instance: object, value: int) -> None | bool:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Value must be between "
                             f"{self.min_value} and {self.max_value}")
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
    def __init__(self,
                 name: str,
                 limitation_class: [SlideLimitationValidator]
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: [Visitor]) -> bool:
        try:
            self.limitation_class(
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height
            )
            return True
        except (ValueError, TypeError):
            return False
