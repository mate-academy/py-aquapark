from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount: int = min_amount
        self.max_amount: int = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.private_name: str = f"_{name}"

    def __get__(self, instance: object, owner: type) -> int:
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Expected int, got {type(value)}")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(f"Value must be between "
                             f"{self.min_amount} and {self.max_amount}")
        setattr(instance, self.private_name, value)


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
    age: IntegerRange = IntegerRange(4, 14)
    height: IntegerRange = IntegerRange(80, 120)
    weight: IntegerRange = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age: IntegerRange = IntegerRange(14, 60)
    height: IntegerRange = IntegerRange(120, 220)
    weight: IntegerRange = IntegerRange(50, 120)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: type[SlideLimitationValidator]
                 ) -> None:
        self.name: str = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except (TypeError, ValueError):
            return False
