from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, instance: object, owner: type) -> int:
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"Value should be between {self.min_amount}"
                f" and {self.max_amount}"
            )
        setattr(instance, self.private_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
        self, age: IntegerRange, weight: IntegerRange, height: IntegerRange
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            IntegerRange(4, 14),
            IntegerRange(20, 50),
            IntegerRange(80, 120)
        )

    def validate(self, visitor: Visitor) -> bool:
        try:
            attributes = ["age", "height", "weight"]
            for attr in attributes:
                min_amount = getattr(self, attr).min_amount
                max_amount = getattr(self, attr).max_amount
                value = getattr(visitor, attr)
                if not (min_amount <= value <= max_amount):
                    return False
        except AttributeError as e:
            print(f"Attribute error: {e}")
            return False
        return True


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            IntegerRange(14, 60),
            IntegerRange(50, 120),
            IntegerRange(120, 220)
        )

    def validate(self, visitor: Visitor) -> bool:
        try:
            attributes = ["age", "height", "weight"]
            for attr in attributes:
                min_amount = getattr(self, attr).min_amount
                max_amount = getattr(self, attr).max_amount
                value = getattr(visitor, attr)
                if not (min_amount <= value <= max_amount):
                    return False
        except AttributeError as e:
            print(f"Attribute error: {e}")
            return False
        return True


class Slide:
    def __init__(
            self, name: str, limitation_class: type(SlideLimitationValidator)
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        validator = self.limitation_class()
        return validator.validate(visitor)
