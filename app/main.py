from abc import ABC, abstractmethod

class IntegerRange:
    def __init__(self, min_amount, max_amount):
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.protected_name = None

    def __get__(self, instance, owner):
        return getattr(instance, self.protected_name)

    def __set__(self, instance, value):
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f'{self.protected_name} should be in range ({self.min_amount}-{self.max_amount})')
        setattr(instance, self.protected_name, value)

    def __set_name__(self, owner, name):
        self.protected_name = f"_{name}"


class Visitor:
    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age_range, height_range, weight_range):
        self.age_range = age_range
        self.height_range = height_range
        self.weight_range = weight_range

    @abstractmethod
    def can_access(self, visitor):
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self):
        age_range = IntegerRange(4, 14)
        height_range = IntegerRange(80, 120)
        weight_range = IntegerRange(20, 50)
        super().__init__(age_range, height_range, weight_range)

    def can_access(self, visitor):
        return (self.age_range.min_amount <= visitor.age <= self.age_range.max_amount and
                self.height_range.min_amount <= visitor.height <= self.height_range.max_amount and
                self.weight_range.min_amount <= visitor.weight <= self.weight_range.max_amount)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self):
        age_range = IntegerRange(14, 60)
        height_range = IntegerRange(120, 220)
        weight_range = IntegerRange(50, 120)
        super().__init__(age_range, height_range, weight_range)

    def can_access(self, visitor):
        return (self.age_range.min_amount <= visitor.age <= self.age_range.max_amount and
                self.height_range.min_amount <= visitor.height <= self.height_range.max_amount and
                self.weight_range.min_amount <= visitor.weight <= self.weight_range.max_amount)


class Slide:
    def __init__(self, name, limitation_class):
        self.name = name
        self.limitation = limitation_class()

    def can_access(self, visitor):
        return self.limitation.can_access(visitor)