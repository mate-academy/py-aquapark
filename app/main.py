from __future__ import annotations

from abc import ABC, abstractmethod

from typing import Type, Any


class IntegerRange:
    def __init__(
            self,
            min_amount: int,
            max_amount: int
    ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def in_range(self, value: Any) -> bool:
        return self.min_amount <= value <= self.max_amount

    def __get__(
            self,
            instance: Any,
            owner: Any
    ) -> int:
        return getattr(instance, self.name)

    def __set__(
            self,
            instance: Any,
            value: int
    ) -> None:
        if not isinstance(value, int):
            raise TypeError("value should be integer")

        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError("value should be in the defined range")

        setattr(instance, self.name, value)

    def __set_name__(
            self,
            owner: Any,
            name: str
    ) -> None:
        self.name = name


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: Type[IntegerRange],
            weight: Type[IntegerRange],
            height: Type[IntegerRange]
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def validate(self, visitor: Visitor) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            IntegerRange(4, 14),
            IntegerRange(20, 50),
            IntegerRange(80, 120)
        )

    @classmethod
    def age(cls) -> Any:
        return cls().age

    @classmethod
    def height(cls) -> Any:
        return cls().height

    @classmethod
    def weight(cls) -> Any:
        return cls().weight

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age.in_range(visitor.age)
            and self.height.in_range(visitor.height)
            and self.weight.in_range(visitor.weight)
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            IntegerRange(14, 60),
            IntegerRange(50, 120),
            IntegerRange(120, 220)
        )

    @classmethod
    def age(cls) -> Any:
        return cls().age

    @classmethod
    def height(cls) -> Any:
        return cls().height

    @classmethod
    def weight(cls) -> Any:
        return cls().weight

    def validate(self, visitor: Visitor) -> bool:
        return (
            self.age.in_range(visitor.age)
            and self.height.in_range(visitor.height)
            and self.weight.in_range(visitor.weight)
        )


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.validate(visitor)
