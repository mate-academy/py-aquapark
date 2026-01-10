from abc import ABC, abstractmethod
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self._name = None

    def __set_name__(self, owner: Any, name: str) -> None:
        self._name = f"_{name}"

    def __get__(self, instance: Any, owner: Any) -> Any:
        if instance is None:
            return self
        return getattr(instance, self._name, self)

    def __set__(self, instance: Any, value: int) -> None:
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"{value} is not in range [{self.min_amount}, "
                f"{self.max_amount}]"
            )
        setattr(instance, self._name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    @abstractmethod
    def validate(self, visitor: Visitor) -> bool:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def validate(self, visitor: Visitor) -> bool:
        return (
            type(self).age.min_amount <= visitor.age
            <= type(self).age.max_amount
            and type(self).height.min_amount <= visitor.height
            <= type(self).height.max_amount
            and type(self).weight.min_amount <= visitor.weight
            <= type(self).weight.max_amount
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def validate(self, visitor: Visitor) -> bool:
        return (
            type(self).age.min_amount <= visitor.age
            <= type(self).age.max_amount
            and type(self).height.min_amount <= visitor.height
            <= type(self).height.max_amount
            and type(self).weight.min_amount <= visitor.weight
            <= type(self).weight.max_amount
        )


class Slide:
    def __init__(self, name: str,
                 limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        # підтримка як класу, так і інстансу
        if isinstance(limitation_class, type):
            self.limitation_validator = limitation_class()
        else:
            self.limitation_validator = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_validator.validate(visitor)
