from abc import ABC


class IntegerRange:
    def __init__(
            self,
            min_amount: int,
            max_amount: int
    ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.name = None

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        pass

    def __get__(
            self,
            obj: object,
            objtype: type | None = None
    ) -> None:
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(
            self,
            obj: object,
            value: int
    ) -> None:
        if type(value) is not int:
            raise TypeError
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError
        obj.__dict__[self.name] = value

        pass


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
    pass


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height
    pass


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height
    pass


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: type
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(
            self,
            visitor: Visitor
    ) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except (TypeError, ValueError):
            return False
