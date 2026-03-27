from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.protected_name = None

    def __set_name__(self, owner: "IntegerRange", name: str) -> None:
        self.protected_name = "_" + name

    def __get__(
            self,
            instance: "SlideLimitationValidator",
            owner: "IntegerRange"
    ) -> int | float:
        return getattr(instance, self.protected_name)

    def __set__(
            self,
            instance: "SlideLimitationValidator",
            value: int
    ) -> None:

        if not isinstance(value, (int, float)):
            raise TypeError
        elif not self.min_amount <= value <= self.max_amount:
            raise ValueError
        else:
            setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            height: int | float,
            weight: int | float
    ) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int,
            height: int | float,
            weight: int | float
    ) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(
            self,
            age: int,
            height: int | float,
            weight: int | float
    ) -> None:
        super().__init__(age, height, weight)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def __init__(
            self,
            age: int,
            height: int | float,
            weight: int | float
    ) -> None:
        super().__init__(age, height, weight)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: type[SlideLimitationValidator]
    ) -> None:

        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.height, visitor.weight)
            return True
        except (TypeError, ValueError):
            return False
