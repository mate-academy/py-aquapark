from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(
            self,
            instance: object,
            owner: object
    ) -> int | float | None:
        return getattr(instance, self.private_name)

    def __set__(
            self,
            instance: object,
            value: int | float
    ) -> int | float | None:
        if self.min_amount <= value <= self.max_amount:
            return setattr(instance, self.private_name, value)
        return setattr(instance, self.private_name, None)

    def __set_name__(self, owner: object, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name


class Visitor:
    def __init__(
        self,
        name: str,
        age: int,
        weight: int | float,
        height: int | float
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int,
            weight: int | float,
            height: int | float
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(
            self,
            age: int,
            weight: int | float,
            height: int | float
    ) -> None:
        super().__init__(age=age, weight=weight, height=height)


class AdultSlideLimitationValidator(
    SlideLimitationValidator
):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(
            self,
            age: int,
            weight: int | float,
            height: int | float
    ) -> None:
        super().__init__(age=age, weight=weight, height=height)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: SlideLimitationValidator
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        visitor_access = self.limitation_class(
            visitor.age,
            visitor.weight,
            visitor.height
        )
        if (visitor_access.age
                and visitor_access.weight
                and visitor_access.height):
            return True
        return False
