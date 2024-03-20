from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object, owner: object) -> int:
        return getattr(instance, self._name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("Value must be an integer")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(f"Value must be between {self.min_amount}"
                             f" and {self.max_amount}")
        setattr(instance, self._name, value)

    def __set_name__(self, owner: object, name: str) -> None:
        self._name = f"_{name}"


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
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
    def __init__(
            self,
            name: str,
            limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_validator = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_validator(
                visitor.age,
                visitor.weight,
                visitor.height
            )
        except (TypeError, ValueError):
            return False
        return True
