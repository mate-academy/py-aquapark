from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object, owner: type) -> None:
        return instance.__dict__[self.name]

    def __set__(self, instance: object, value: int) -> None:
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(f"{self.name} must be between "
                             f"{self.min_amount} and {self.max_amount}")
        instance.__dict__[self.name] = value

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height

    age: IntegerRange = IntegerRange(0, 150)
    weight: IntegerRange = IntegerRange(0, 500)
    height: IntegerRange = IntegerRange(0, 300)


class SlideLimitationValidator(ABC):
    def __init__(self, age: tuple, weight: tuple, height: tuple) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age=(4, 14), weight=(20, 50), height=(80, 120))

    def validate(self, visitor: Visitor) -> bool:
        if (
            self.age[0] <= visitor.age <= self.age[1]
            and self.weight[0] <= visitor.weight <= self.weight[1]
            and self.height[0] <= visitor.height <= self.height[1]
        ):
            return True
        return False


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age=(14, 60), weight=(50, 120), height=(120, 220))

    def validate(self, visitor: Visitor) -> bool:
        if (
            self.age[0] <= visitor.age <= self.age[1]
            and self.weight[0] <= visitor.weight <= self.weight[1]
            and self.height[0] <= visitor.height <= self.height[1]
        ):
            return True
        return False


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class().validate(visitor)
