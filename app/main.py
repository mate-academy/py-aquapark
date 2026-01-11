from abc import ABC
from typing import Any, Type


class IntegerRange:
    """Дескриптор для валідації цілочисельних значень у заданому діапазоні."""

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.public_name: str
        self.private_name: str

    def __set_name__(self, owner: Type[Any], name: str) -> None:
        """Визначає публічне та приватне ім'я для зберігання даних."""
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, instance: Any, owner: Type[Any]) -> Any:
        """Отримує значення з екземпляра."""
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance: Any, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")

        # E501: Рядок був розділений, щоб не перевищувати 79 символів
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"{self.public_name} must be between {self.min_amount} "
                f"and {self.max_amount}"
            )
        setattr(instance, self.private_name, value)


class Visitor:
    """Модель відвідувача з основними характеристиками."""

    # E302: Додано два порожні рядки перед визначенням класу.
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        # E231: Додано пробіли після ком
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
    """Валідатор для дитячої гірки."""
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    """Валідатор для дорослої гірки."""
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)


class Slide:
    """Модель гірки, яка перевіряє доступність для відвідувача."""

    # E302: Додано два порожні рядки перед визначенням класу.
    def __init__(
        self, name: str, limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        # E231: Додано пробіли після ком
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except Exception:
            return False
