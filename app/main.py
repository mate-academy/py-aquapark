from abc import ABC


class IntegerRange:
    def __init__(
        self,
        min_amount: int,
        max_amount: int,
    ):
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.private_name = None

    def __set_name__(
        self,
        owner,
        name,
    ):
        self.private_name = f"_{name}"

    def __get__(
        self,
        instance,
        owner,
    ):
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def validate(
        self,
        value,
    ):
        if not isinstance(value, int):
            raise TypeError

        if not self.min_amount <= value <= self.max_amount:
            raise ValueError

    def __set__(
        self,
        instance,
        value,
    ):
        self.validate(value)
        setattr(instance, self.private_name, value)


class Visitor:
    def __init__(
        self,
        name: str,
        age: int,
        weight: int,
        height: int,
    ):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
        self,
        age: int,
        weight: int,
        height: int,
    ):
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
    def __init__(
        self,
        name: str,
        limitation_class,
    ):
        self.name = name
        self.limitation_class = limitation_class

    def can_access(
        self,
        visitor: Visitor,
    ) -> bool:
        try:
            self.limitation_class(
                age=visitor.age,
                weight=visitor.weight,
                height=visitor.height,
            )
            return True
        except (TypeError, ValueError):
            return False
