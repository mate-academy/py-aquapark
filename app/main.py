from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, cls: object, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, instance: object, cls: object) -> (int, str):
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: (int, str)) -> None:
        """if not (self.min_amount <= value <= self.max_amount):
            raise ValueError("ValueError")"""
        setattr(instance, self.private_name, value)


class Visitor:
    age = IntegerRange(4, 60)
    weight = IntegerRange(20, 120)
    height = IntegerRange(80, 220)

    def __init__(self,
                 name: str,
                 age: int,
                 height: float,
                 weight: float) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: float, height: float) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def validate(self) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self, age: int, weight: float, height: float) -> None:
        super().__init__(age, weight, height)

    def validate(self) -> bool:
        return (4 <= self.age <= 14
                and 20 <= self.weight <= 50
                and 80 <= self.height <= 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self, age: int, weight: float, height: float) -> None:
        super().__init__(age, weight, height)

    def validate(self) -> bool:
        return (14 <= self.age <= 60
                and 50 <= self.weight <= 120 <= self.height <= 220)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: [ChildrenSlideLimitationValidator,
                                    AdultSlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age,
                                  visitor.weight,
                                  visitor.height)
        except ValueError:
            ...
        obj = self.limitation_class(visitor.age,
                                    visitor.weight,
                                    visitor.height)
        return obj.validate()
