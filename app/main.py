from __future__ import annotations

from abc import ABC


class IntegerRange:

    def __init__(self,
                 min_amount: int,
                 max_amount: int,
                 ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self,
                     owner: type,
                     name: str,
                     ) -> None:
        self.protected_name = f"_{name}"

    def __get__(self,
                instance: any,
                owner: type,
                ) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self,
                instance: any,
                value: int | str,
                ) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.protected_name, value)
        else:
            raise ValueError(f"Value {value} out of range: "
                             f"{self.min_amount} - {self.max_amount}")


class Visitor:
    def __init__(self,
                 name: str,
                 age: int,
                 weight: float | int,
                 height: float | int,
                 ) -> None:
        self.height = height
        self.weight = weight
        self.age = age
        self.name = name


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age: int,
                 weight: float | int,
                 height: float | int,
                 ) -> None:
        self.height = height
        self.weight = weight
        self.age = age


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
                 name: str,  # slide's name
                 limitation_class: type,
                 ) -> None:
        self.limitation_class = limitation_class
        self.name = name

    def can_access(self, instance: Visitor) -> bool:
        try:
            self.limitation_class(age=instance.age,
                                  weight=instance.weight,
                                  height=instance.height)
        except ValueError:
            return False
        return True
