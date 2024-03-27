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
        super().__init__(
            age=IntegerRange(4, 14),
            weight=IntegerRange(20, 50),
            height=IntegerRange(80, 120)
        )


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
        self.limitation_validator = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        if not isinstance(visitor, Visitor):
            raise TypeError("Visitor must be an instance of Visitor class.")
        return all([
            self.limitation_validator.age.min_amount
            <= visitor.age <= self.limitation_validator.age.max_amount,
            self.limitation_validator.height.min_amount
            <= visitor.height <= self.limitation_validator.height.max_amount,
            self.limitation_validator.weight.min_amount
            <= visitor.weight <= self.limitation_validator.weight.max_amount
        ])
