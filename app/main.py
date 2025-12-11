from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: type[object]) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> int:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        elif value not in range(self.min_amount, self.max_amount + 1):
            raise ValueError(
                f"Value must be between "
                f"{self.min_amount} and {self.max_amount}"
            )
        else:
            setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


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
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
        except (TypeError, ValueError):
            return False
        else:
            return True
