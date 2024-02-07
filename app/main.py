from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object, owner: type) -> tuple[int, int]:
        return self.min_value, self.max_value

    def __set__(self, instance: object, value: str) -> None:
        self.min_value, self.max_value = value


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: IntegerRange,
                 weight: IntegerRange, height: IntegerRange) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def validate(self, visitor: Visitor) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age=IntegerRange(4, 14),
                         height=IntegerRange(80, 120),
                         weight=IntegerRange(20, 50))

    def validate(self, visitor: Visitor) -> bool:
        return (self.age.min_value <= visitor.age <= self.age.max_value
                and self.height.min_value <= visitor.height
                <= self.height.max_value
                and self.weight.min_value <= visitor.weight
                <= self.weight.max_value)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age=IntegerRange(14, 60),
                         height=IntegerRange(120, 220),
                         weight=IntegerRange(50, 120))

    def validate(self, visitor: Visitor) -> bool:
        return (self.age.min_value <= visitor.age <= self.age.max_value
                and self.height.min_value <= visitor.height
                <= self.height.max_value
                and self.weight.min_value <= visitor.weight
                <= self.weight.max_value)


class Slide:
    def __init__(self, name: str,
                 limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> None:
        return self.limitation_class.validate(visitor)
