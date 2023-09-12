from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: callable, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: callable, owner: callable) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: callable, value: int) -> None:
        if value in range(self.min_amount, self.max_amount + 1):
            setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, height: int, weight: int) -> None:
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
    def __init__(self,
                 name: str,
                 limitation_class: SlideLimitationValidator
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, client: Visitor) -> bool:
        return len(self.limitation_class(
            client.age,
            client.height,
            client.weight).__dict__) == len(client.__dict__) - 1
