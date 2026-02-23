from abc import ABC
from typing import Type


# Дескриптор з перевіркою типу і діапазону
class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount: int = min_amount
        self.max_amount: int = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.private_name: str = f"_{name}"

    def __get__(self, instance: object, owner: type) -> int:
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"Value must be in range "
                             f"{self.min_amount}–{self.max_amount}")
        setattr(instance, self.private_name, value)


# Клас відвідувача
class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name: str = name
        self.age: int = age
        self.weight: int = weight
        self.height: int = height


# Базовий клас для обмежень гірок
class SlideLimitationValidator(ABC):
    age: IntegerRange
    weight: IntegerRange
    height: IntegerRange

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


# Обмеження для дітей
class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age: IntegerRange = IntegerRange(4, 14)
    height: IntegerRange = IntegerRange(80, 120)
    weight: IntegerRange = IntegerRange(20, 50)


# Обмеження для дорослих
class AdultSlideLimitationValidator(SlideLimitationValidator):
    age: IntegerRange = IntegerRange(14, 60)
    height: IntegerRange = IntegerRange(120, 220)
    weight: IntegerRange = IntegerRange(50, 120)


# Гірка
class Slide:
    def __init__(self, name: str,
                 limitation_class: Type[SlideLimitationValidator]) -> None:
        self.name: str = name
        self.limitation_class: Type[SlideLimitationValidator] = (
            limitation_class)

    def can_access(self, visitor: Visitor) -> bool:
        try:
            # створення обʼєкта обмеження для перевірки атрибутів відвідувача
            self.limitation_class(
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height
            )
            return True
        except (TypeError, ValueError):
            return False
