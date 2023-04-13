from __future__ import annotations

from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: SlideLimitationValidator, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(
            self,
            instance: SlideLimitationValidator,
            owner: SlideLimitationValidator
    ) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: SlideLimitationValidator, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"Value {self.public_name} must be in range "
                f"{self.min_amount} - {self.max_amount}"
            )
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height

    def __str__(self) -> str:
        return f"{self.name}, {self.age} years old."


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(min_amount=4, max_amount=14)
    weight = IntegerRange(min_amount=20, max_amount=50)
    height = IntegerRange(min_amount=80, max_amount=120)

    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(min_amount=14, max_amount=60)
    weight = IntegerRange(min_amount=50, max_amount=120)
    height = IntegerRange(min_amount=120, max_amount=220)

    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
        super().__init__(age, weight, height)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: type(SlideLimitationValidator)
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, guest: Visitor) -> bool:
        try:
            self.limitation_class(guest.age, guest.weight, guest.height)
        except ValueError:
            return False
        return True
