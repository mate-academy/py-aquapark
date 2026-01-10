from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: str, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, obj: str, objtype: None = None) -> int:
        amount = getattr(obj, self.private_name)
        return amount

    def __set__(self, obj: str, amount: int) -> None:
        if not isinstance(amount, int):
            raise TypeError
        if amount < self.min_amount or amount > self.max_amount:
            raise ValueError
        setattr(obj, self.private_name, amount)


class Visitor:
    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            instance = self.limitation_class()
            instance.age = visitor.age
            instance.height = visitor.height
            instance.weight = visitor.weight
            return True
        except (TypeError, ValueError):
            return False
