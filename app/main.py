from abc import ABC


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Visitor, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, instance: Visitor, value: int) -> str:
        return getattr(instance, self.private_name)

    def __set__(self, instance: Visitor, value: int) -> None:
        if value != -1 and not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"Value {value} is out of range - "
                f"{self.min_amount} - {self.max_amount}"
            )
        setattr(instance, self.private_name, value)


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int = -1,
            weight: int = -1,
            height: int = -1
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: type
    ) -> None:
        self.name = name
        self.limitation = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation.age = visitor.age
            self.limitation.weight = visitor.weight
            self.limitation.height = visitor.height
        except ValueError:
            return False
        return True
