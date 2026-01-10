from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.protected_name = None

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: type) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Value should be integer.")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"Value should not be less than"
                f" {self.min_amount} and greater than {self.max_amount}."
            )
        setattr(instance, self.protected_name, value)


class Visitor:
    age = IntegerRange(0, 100)
    weight = IntegerRange(10, 200)
    height = IntegerRange(50, 250)

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

    @abstractmethod
    def validate(self, visitor: str) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(IntegerRange(4, 14),
                         IntegerRange(20, 50), IntegerRange(80, 120))

    def validate(self, visitor: str) -> bool:
        return (self.age.min_amount <= visitor.age <= self.age.max_amount
                and self.weight.min_amount <= visitor.weight
                <= self.weight.max_amount
                and self.height.min_amount <= visitor.height
                <= self.height.max_amount)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(IntegerRange(14, 60),
                         IntegerRange(50, 120), IntegerRange(120, 220))

    def validate(self, visitor: str) -> bool:
        return (self.age.min_amount <= visitor.age <= self.age.max_amount
                and self.weight.min_amount <= visitor.weight
                <= self.weight.max_amount
                and self.height.min_amount <= visitor.height
                <= self.height.max_amount)


class Slide:
    def __init__(self, name: str, limitation_class: str) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: str) -> None:
        return self.limitation_class().validate(visitor)
