from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: type, owner: type) -> None:
        return instance.__dict__[self.name]

    def __set__(self, instance: type, value: type) -> None:
        if self.min_amount <= value <= self.max_amount:
            instance.__dict__[self.name] = value
        else:
            raise ValueError(f"{self.name} must be between "
                             f"{self.min_amount} and {self.max_amount}")

    def __set_name__(self, owner: None, name: str) -> None:
        self.name = name


class Visitor:
    def __init__(self, name: str, age: int,
                 weight: float, height: float) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age_min: int, age_max: int,
                 weight_min: float, weight_max: float, height_min: float,
                 height_max: float) -> None:
        self.age_min = age_min
        self.age_max = age_max
        self.weight_min = weight_min
        self.weight_max = weight_max
        self.height_min = height_min
        self.height_max = height_max

    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age_min=4, age_max=14,
                         weight_min=20.0, weight_max=50.0,
                         height_min=80.0, height_max=120.0)

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age_min <= visitor.age <= self.age_max
            and self.weight_min <= visitor.weight <= self.weight_max
            and self.height_min <= visitor.height <= self.height_max
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age_min=14, age_max=60,
                         weight_min=50.0, weight_max=120.0,
                         height_min=120.0, height_max=220.0)

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age_min <= visitor.age <= self.age_max
            and self.weight_min <= visitor.weight <= self.weight_max
            and self.height_min <= visitor.height <= self.height_max
        )


class Slide:
    def __init__(self, name: str,
                 limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.validate(visitor)
