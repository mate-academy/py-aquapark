from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"{self.protected_name} should be an integer")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"{self.protected_name} should be between "
                             f"{self.min_amount} and {self.max_amount}")
        setattr(instance, self.protected_name, value)

    def __get__(self, instance: object, owner: type) -> int:
        return getattr(instance, self.protected_name)

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name


class Visitor:
    age = IntegerRange(0, 100)
    height = IntegerRange(0, 300)
    weight = IntegerRange(0, 300)

    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def __init__(self, age: tuple, weight: tuple, height: tuple) -> None:
        self.age = IntegerRange(*age)
        self.weight = IntegerRange(*weight)
        self.height = IntegerRange(*height)


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age=(4, 14), weight=(20, 50), height=(80, 120))


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age=(14, 60), weight=(50, 120), height=(120, 220))


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: type(SlideLimitationValidator)
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return (self.limitation_class.age.min_amount <= visitor.age
                <= self.limitation_class.age.max_amount
                and self.limitation_class.weight.min_amount
                <= visitor.weight <= self.limitation_class.weight.max_amount
                and self.limitation_class.height.min_amount <= visitor.height
                <= self.limitation_class.height.max_amount)
