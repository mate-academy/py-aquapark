from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: type[object]) -> int:
        value = getattr(instance, self.protected_name)
        return value

    def __set__(self, instance: object, value: int) -> ValueError | None:
        if value < self.min_amount or value > self.max_amount:
            raise ValueError
        setattr(instance, self.protected_name, value)


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
    def __init__(
            self, name: str, limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, obj: Visitor) -> bool:
        try:
            self.limitation_class(
                age=obj.age, height=obj.height, weight=obj.weight
            )
        except ValueError:
            return False
        return True
