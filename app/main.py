from abc import ABC


class IntegerRange:
    def __init__(
            self, min_amount: int, max_amount: int
    ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(
            self, owner: type, name: str
    ) -> None:
        self.name = f"_{name}"

    def __get__(
            self, instance: object, owner: type
    ) -> int | None:
        if instance is None:
            return self
        return getattr(
            instance, self.name, None
        )

    def __set__(
            self, instance: object, value: int
    ) -> None:
        if not isinstance(
                value, int
        ) or isinstance(value, bool):
            raise TypeError(
                "Value must be integer"
            )
        if not (
                self.min_amount
                <= value
                <= self.max_amount
        ):
            raise ValueError(
                "Value out of range"
            )
        setattr(instance, self.name, value)


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            weight: int,
            height: int,
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(
            self,
            age: int,
            height: int,
            weight: int,
    ) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(
            self,
            age: int,
            height: int,
            weight: int,
    ) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: type[
                SlideLimitationValidator
            ],
    ) -> None:
        self.name = name
        self.limitation_class = (
            limitation_class
        )

    def can_access(
            self, visitor: Visitor
    ) -> bool:
        try:
            self.limitation_class(
                age=visitor.age,
                height=visitor.height,
                weight=visitor.weight,
            )
            return True
        except (TypeError, ValueError):
            return False
