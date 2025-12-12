from abc import ABC


class IntegerRange:

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: "Visitor", name: str) -> None:
        self._protected_name = "_" + name

    def __get__(self, obj: "Visitor", objtype: any) -> object:
        return getattr(obj, self._protected_name)

    def __set__(self, obj: "Visitor", value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"{value} must be an integer.")
        if self.min_amount is not None and value < self.min_amount:
            raise ValueError(f"{value} must be greater than min_amount.")
        if self.max_amount is not None and value > self.max_amount:
            raise ValueError(f"{value} must be less than max_amount.")
        else:
            setattr(obj, self._protected_name, value)


class Visitor:

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:

    def __init__(self, name: str, limitation_class: any) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except (TypeError, ValueError):
            return False
