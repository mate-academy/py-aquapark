from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: any, name: str) -> None:
        self.protect_name = "_" + name

    def __get__(self, instance: any, owner: any) -> str:
        return getattr(instance, self.protect_name)

    def __set__(self, instance: any, value: str) -> None:
        if not isinstance(value, int):
            return ValueError
        if self.min_amount > value or value > self.max_amount:
            raise TypeError

        setattr(instance, self.protect_name, value)


class Visitor:
    age = IntegerRange
    height = IntegerRange
    weight = IntegerRange

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
            height: int,
            weight: int
    ) -> None:
        self.age = age
        self.height = height
        self.weight = weight


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

    def can_access(self, visitant: any) -> bool:
        try:
            self.limitation_class(
                age=visitant.age,
                height=visitant.height,
                weight=visitant.weight
            )
            return True
        except TypeError:
            return False
