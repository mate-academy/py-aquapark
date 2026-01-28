from abc import ABC


class IntegerRange(ABC):
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.protected_name = None

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: "Visitor", owner: type["Visitor"]) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: "Visitor", value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"Value must be between {self.min_amount} "
                f"and {self.max_amount}"
            )
        setattr(instance, self.protected_name, value)


class Visitor:
    age = IntegerRange(0, 100)
    weight = IntegerRange(0, 200)
    height = IntegerRange(0, 250)

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def is_valid(self, visitor: Visitor) -> bool:
        raise NotImplementedError


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def is_valid(self, visotor: Visitor) -> bool:
        return (
            4 <= visotor.age <= 14
            and 80 <= visotor.height <= 120
            and 20 <= visotor.weight <= 50
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def is_valid(self, visotor: Visitor) -> bool:
        return (
            14 <= visotor.age <= 60
            and 120 <= visotor.height <= 220
            and 50 <= visotor.weight <= 120
        )


class Slide:
    def __init__(
        self, name: str, limitation_class: type["SlideLimitationValidator"]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        limitation = self.limitation_class()
        return limitation.is_valid(visitor)
