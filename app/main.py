from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: type) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if isinstance(value, int):
            if self.min_amount <= value <= self.max_amount:
                setattr(instance, self.protected_name, value)
                return


class Visitor:
    age = IntegerRange(4, 60)
    height = IntegerRange(80, 220)
    weight = IntegerRange(20, 120)

    def __init__(
            self, name: str, age: int, height: int, weight: int
    ) -> None:
        self._name = name
        self._age = age
        self._height = height
        self._weight = weight


class SlideLimitationValidator(ABC):
    def __init__(
            self, age_range: tuple, height_range: tuple, weight_range: tuple
    ) -> None:
        self.age_range = age_range
        self.height_range = height_range
        self.weight_range = weight_range

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age_range[0] <= visitor.age <= self.age_range[1]
            and self.weight_range[0] <= visitor.weight <= self.weight_range[1]
            and self.height_range[0] <= visitor.height <= self.height_range[1]
        )


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__((4, 14), (80, 120), (20, 50))


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__((14, 60), (120, 220), (50, 120))


class Slide:
    def __init__(
            self, name: str,
            limitation_class: type
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.validate(visitor)
