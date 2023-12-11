from __future__ import annotations
from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(
            self,
            min_amount: int,
            max_amount: int
    ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(
            self,
            owner: SlideLimitationValidator,
            name: str
    ) -> None:
        self.private_name = "_" + name
        self.public_name = name

    def __get__(
            self,
            instance: SlideLimitationValidator,
            owner: Slide
    ) -> int:
        return getattr(instance, self.private_name)

    def __set__(
            self,
            instance: SlideLimitationValidator,
            value: int
    ) -> None:
        if instance.validate(value, self.min_amount, self.max_amount):
            setattr(instance, self.private_name, value)
        else:
            setattr(instance, self.private_name, False)


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
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def validate(
            self,
            value: int,
            min_value: int,
            max_value: int
    ) -> bool:
        return isinstance(value, int) and min_value <= value <= max_value


class ChildrenSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
        super().__init__(age, weight, height)

    def validate(
            self,
            value: int,
            min_value: int,
            max_value: int
    ) -> bool:
        return super().validate(value, min_value, max_value)


class AdultSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
        super().__init__(age, weight, height)

    def validate(
            self,
            value: int,
            min_value: int,
            max_value: int
    ) -> bool:
        return super().validate(value, min_value, max_value)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, instance: Visitor) -> bool:
        visitor = self.limitation_class(
            age=instance.age,
            weight=instance.weight,
            height=instance.height
        )

        return (
            True if visitor.age and visitor.weight and visitor.height
            else False
        )
