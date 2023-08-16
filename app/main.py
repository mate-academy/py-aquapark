from abc import ABC


class IntegerRange:
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __get__(self, instance: object, owner: object) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if self.min_value <= value <= self.max_value:
            setattr(instance, self.protected_name, value)
        else:
            raise ValueError(f"Value should be greater than {self.min_value} "
                             f"and lower than {self.max_value}")

    def __set_name__(self, owner: object, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
        self,
        age: IntegerRange,
        weight: IntegerRange,
        height: IntegerRange
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
    def __init__(
        self,
        name: str,
        limitation_class: [SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except ValueError:
            return False
