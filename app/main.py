from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: type, name: str) -> None:
        self.private_name = f"__{name}"

    def __get__(self, obj: object, object_type: type | None = None) -> object:
        return getattr(obj, self.private_name)

    def __set__(self, obj: object, value: int) -> None:
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value: int) -> None:
        pass


class IntegerRange(Validator):
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be an integer.")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"Value {value} must be between "
                f"{self.min_amount} and {self.max_amount}."
            )


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
    def __init__(
        self,
        name: str,
        limitation_class: type[SlideLimitationValidator],
    ) -> None:
        if issubclass(limitation_class, SlideLimitationValidator):
            self.limitation_class = limitation_class
            self.name = name
        else:
            raise TypeError(
                "limitation_class must be subclass of "
                "SlideLimitationValidator."
            )

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                age=visitor.age,
                height=visitor.height,
                weight=visitor.weight,
            )
            return True
        except Exception:
            return False
