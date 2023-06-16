from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount, max_amount):
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if self.min_amount <= value <= self.max_amount:
            instance.__dict__[self.name] = value
        else:
            raise ValueError(f"Value must be between {self.min_amount} and {self.max_amount}")

    def __set_name__(self, owner, name):
        self.name = name


class Visitor:
    age = IntegerRange(0, 150)
    weight = IntegerRange(0, 500)
    height = IntegerRange(0, 300)

    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age, weight, height):
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def can_access(self, visitor):
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self):
        super().__init__(age=IntegerRange(4, 14), weight=IntegerRange(20, 50), height=IntegerRange(80, 120))

    def can_access(self, visitor):
        return (
            self.age.min_amount <= visitor.age <= self.age.max_amount and
            self.weight.min_amount <= visitor.weight <= self.weight.max_amount and
            self.height.min_amount <= visitor.height <= self.height.max_amount
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self):
        super().__init__(age=IntegerRange(14, 60), weight=IntegerRange(50, 120), height=IntegerRange(120, 220))

    def can_access(self, visitor):
        return (
            self.age.min_amount <= visitor.age <= self.age.max_amount and
            self.weight.min_amount <= visitor.weight <= self.weight.max_amount and
            self.height.min_amount <= visitor.height <= self.height.max_amount
        )


class Slide:
    def __init__(self, name, limitation_class):
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor):
        limitation_validator = self.limitation_class()
        return limitation_validator.can_access(visitor)
