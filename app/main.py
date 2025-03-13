from abc import ABC
from typing import Any, Type


class IntegerRange:
    """Дескриптор для проверки целых чисел в заданном диапазоне."""

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> None:
        """Метод для установки имени атрибута."""
        self.protected_name = f"_{name}"

    def __get__(self, instance: Any, owner: Any) -> Any:
        """Метод для получения значения атрибута."""
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        """Метод для установки значения атрибута."""
        if not isinstance(value, int):
            raise TypeError("Value must be an integer.")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"Value must be between {self.min_amount}"
                f" and {self.max_amount}."
            )
        setattr(instance, self.protected_name, value)


class Visitor:
    """Класс для хранения данных посетителя."""

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        """Инициализация данных посетителя."""
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    """Базовый класс для валидаторов ограничений горок."""

    def __init__(self, age: int, weight: int, height: int) -> None:
        """Инициализация валидатора с параметрами посетителя."""
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    """Валидатор для детских горок."""

    age = IntegerRange(min_amount=4, max_amount=14)
    height = IntegerRange(min_amount=80, max_amount=120)
    weight = IntegerRange(min_amount=20, max_amount=50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    """Валидатор для взрослых горок."""

    age = IntegerRange(min_amount=14, max_amount=60)
    height = IntegerRange(min_amount=120, max_amount=220)
    weight = IntegerRange(min_amount=50, max_amount=120)


class Slide:
    """Класс для представления водной горки."""

    def __init__(
        self, name: str, limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        """Инициализация горки с названием и классом ограничений."""
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        """Проверка, может ли посетитель использовать горку."""
        try:
            self.limitation_class(
                age=visitor.age, weight=visitor.weight, height=visitor.height
            )
            return True
        except (TypeError, ValueError):
            return False
