from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: str, name: str) -> None:
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, instance: object, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(
                f"O atributo '{self.public_name}' "
                f"deve ser um número inteiro.")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"O valor {value} para '{self.public_name}' "
                f"está fora do intervalo permitido "
                f"[{self.min_amount}, {self.max_amount}]."
            )

    def __set__(self, instance: Any, value: int) -> None:
        self.validate(value)
        setattr(instance, self.private_name, value)


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
        except (TypeError, ValueError):
            return False
