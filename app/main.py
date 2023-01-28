from __future__ import annotations
from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, max_amount: int, min_amount: int) -> None:
        self.max_amount = max_amount
        self.min_amount = min_amount

    def __set_name__(self, owner: Visitor, name) -> str:
        self._protected_name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self._protected_name)

    def __set__(self, instance: Visitor, value: int) -> None:
        if self.max_amount < value or value < self.min_amount:
            raise ValueError(f"{self._protected_name} has_access "
                             f"for visitor with such parameters:"
                             f" (age: {instance.age},weight: {instance.weight}"
                             f"height: {instance.height}. ")
        else:
            setattr(instance, self._protected_name, value)

class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int,
            weight: int,
            height: int,
    ):
        self.age = age
        self.weight = weight
        self.height = height

class ChildrenSlideLimitationValidator(
SlideLimitationValidator
):
    _age = IntegerRange(4, 14)
    _height = IntegerRange(80, 120)
    _weight = IntegerRange(20, 50)

    # def __init__(self, age: int, weight: int, height: int) -> None:
    #     super().__init__(age, weight, height)



class AdultSlideLimitationValidator(SlideLimitationValidator):
    _age = IntegerRange(14, 60)
    _height = IntegerRange(120, 220)
    _weight = IntegerRange(50, 120)
    #
    # def __init__(self, age: int, weight: int, height: int) -> None:
    #     super().__init__(age, weight, height)



class Slide:
    def __init__(
            self, name: str, limitation_class: type[SlideLimitationValidator]

    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor):
        # self.limitation_class = SlideLimitationValidator
        try:
            self.limitation_class(age=visitor.age, height=visitor.height, weight=visitor.weight)
            # return True
        except ValueError:
            print("some error")
            return False
        return True


