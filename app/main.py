from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: object, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, obj: object, objtype: None) -> int:
        value = getattr(obj, self.private_name)
        return value

    def __set__(self, obj: object, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("Value must be integer.")
        elif not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"Value must be between {self.min_amount}"
                f" and {self.max_amount}"
            )
        setattr(obj, self.private_name, value)


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


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        self.age = IntegerRange(4, 14)
        self.height = IntegerRange(80, 120)
        self.weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            age=IntegerRange(14, 60),
            weight=IntegerRange(50, 120),
            height=IntegerRange(120, 220)
        )


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        if not isinstance(visitor, Visitor):
            raise TypeError("Visitor must be an instance of Visitor class.")
        return all([
            self.limitation_class.age.min_amount
            <= visitor.age <= self.limitation_class.age.max_amount,
            self.limitation_class.height.min_amount
            <= visitor.height <= self.limitation_class.height.max_amount,
            self.limitation_class.weight.min_amount
            <= visitor.weight <= self.limitation_class.weight.max_amount
        ])
