from abc import ABC
from typing import Any , Type


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner, age) -> None:
        self._age = age

    def __set__(self, instance, value) -> None:
        if not hasattr(instance, '_private_data'):
            instance._private_data = {}

        if not isinstance(value, int):
            raise TypeError(f'Value {value} must be an integer')

        if self.min_amount <= value <= self.max_amount:
            instance._private_data[self._age]= value
        else:
            raise ValueError(f"Value {value} must be between {self.min_amount} and {self.max_amount}")

    def __get__(self, instance, owner) -> object:
        if instance is None:
            return self
        return instance._private_data[self._age]


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
    age = IntegerRange(4,14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height
        super().__init__(age, weight, height)

class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14,60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height
        super().__init__(age, weight, height)

class Slide:
    def __init__(self, name: str, limitation_class: Type[Any]) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                age = visitor.age,
                weight = visitor.weight,
                height = visitor.height
            )
            return True
        except (ValueError, TypeError) as e:
            print(f"Cant access {self.name}: {e}")
            return False
        except Exception as e:
            print(f"Cant access {self.name}: {e}")
            return False
