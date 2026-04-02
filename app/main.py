from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object, owner: type) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if value not in range(self.min_amount, self.max_amount + 1):
            raise ValueError(
                f"Value should be in the range {self.min_amount} "
                f"to {self.max_amount}."
            )
        setattr(instance, self.protected_name, value)

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self._age = age
        self._weight = weight
        self._height = height

    @property
    def age(self) -> int:
        return self._age

    @property
    def weight(self) -> int:
        return self._weight

    @property
    def height(self) -> int:
        return self._height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator, IntegerRange):
    age = IntegerRange(min_amount=4, max_amount=14)
    height = IntegerRange(min_amount=80, max_amount=120)
    weight = IntegerRange(min_amount=20, max_amount=50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(min_amount=14, max_amount=60)
    height = IntegerRange(min_amount=120, max_amount=220)
    weight = IntegerRange(min_amount=50, max_amount=120)


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height
            )
            return True
        except ValueError:
            return False
