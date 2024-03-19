from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: object, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, instance: object, owner: object) -> None:
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"{value}Not in limit! "
                             f"{self.min_amount}... {self.max_amount}")
        setattr(instance, self.private_name, value)


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
                 limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, inst: Visitor) -> bool:
        # if self.limitation_class.__dict__["age"].__dict__["min_amount"] <= inst.age <= self.limitation_class.__dict__["age"].__dict__["max_amount"]:
        #     if self.limitation_class.__dict__["height"].__dict__["min_amount"] <= inst.height <= self.limitation_class.__dict__["height"].__dict__["max_amount"]:
        #         if self.limitation_class.__dict__["weight"].__dict__["min_amount"] <= inst.weight <= self.limitation_class.__dict__["weight"].__dict__["max_amount"]:
        #             return True
        # return False
        try:
            self.limitation_class(inst.age, inst.height, inst.weight)
            return True
        except Exception:
            return False


