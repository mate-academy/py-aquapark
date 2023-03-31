from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: int, value: int) -> str:
        self.value = value

    def __get__(self) -> bool:
        try:
            if self.limitation_class == ChildrenSlideLimitationValidator:
                if (
                        not (4 <= self.age <= 14)
                        or not (80 <= self.height <= 120)
                        or not (20 <= self.weight <= 50)
                ):
                    raise ValueError(
                        "Invalid parameters for accessing children slide"
                    )
            elif self.limitation_class == AdultSlideLimitationValidator:
                if (
                        not (14 <= self.age <= 60)
                        or not (120 <= self.height <= 220)
                        or not (50 <= self.weight <= 120)
                ):
                    raise ValueError(
                        "Invalid parameters for accessing adult slide"
                    )
            return True
        except ValueError:
            return False

    def __set__(self, instance: str) -> str:
        if self.min_amount < self.value > self.max_amount:
            raise ValueError("Invalid value")


class Visitor:
    def __init__(
            self, age: int, height: int, weight: int,
            name: str = ""
    ) -> None:
        self.age = age
        self.height = height
        self.weight = weight
        self.name = name


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(min_amount=4, max_amount=14)
    height = IntegerRange(min_amount=80, max_amount=120)
    weight = IntegerRange(min_amount=20, max_amount=50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(min_amount=14, max_amount=60)
    height = IntegerRange(min_amount=120, max_amount=220)
    weight = IntegerRange(min_amount=50, max_amount=120)


class Slide:
    def __init__(self, name: str, limitation_class: int,) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        self.age = visitor.age
        self.height = visitor.height
        self.weight = visitor.weight
        return IntegerRange.__get__(self)
