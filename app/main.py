from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: type) -> str | int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: any) -> "object":
        if value > self.max_amount or value < self.min_amount:
            raise ValueError
        elif not isinstance(value, int):
            raise TypeError("Incorrect data type!")
        return setattr(instance, self.protected_name, value)


class Visitor:

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    age = None
    weight = None
    height = None

    def __init__(self) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def __init__(self) -> None:
        super().__init__()


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def __init__(self) -> None:
        super().__init__()


class Slide:
    def __init__(
        self, name: str,
        limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        validator = self.limitation_class()
        try:
            validator.age = visitor.age
            validator.height = visitor.height
            validator.weight = visitor.weight
            return True
        except (ValueError, TypeError):
            return False
