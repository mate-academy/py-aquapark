from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount, max_amount):
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.name = None

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"Value must be between {self.min_amount} and {self.max_amount}"
            )
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Visitor:
    age = IntegerRange(0, 150)
    weight = IntegerRange(0, 300)
    height = IntegerRange(0, 300)

    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age_range, weight_range, height_range):
        self.age_range = age_range
        self.weight_range = weight_range
        self.height_range = height_range

    @abstractmethod
    def validate(self, visitor):
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self):
        super().__init__(
            age_range=(4, 14), weight_range=(20, 50), height_range=(80, 120)
        )

    def validate(self, visitor):
        return (
            self.age_range[0] <= visitor.age <= self.age_range[1]
            and self.weight_range[0] <= visitor.weight <= self.weight_range[1]
            and self.height_range[0] <= visitor.height <= self.height_range[1]
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self):
        super().__init__(
            age_range=(14, 60), weight_range=(50, 120), height_range=(120, 220)
        )

    def validate(self, visitor):
        return (
            self.age_range[0] <= visitor.age <= self.age_range[1]
            and self.weight_range[0] <= visitor.weight <= self.weight_range[1]
            and self.height_range[0] <= visitor.height <= self.height_range[1]
        )


class Slide:
    def __init__(self, name, limitation_class):
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor):
        return self.limitation_class.validate(visitor)
