from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set__(self, instance: object, value: type) -> None:
        if not isinstance(value, int):
            raise ValueError("Value must be an integer.")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"Value must be between {self.min_amount}"
                f"and {self.max_amount}."
            )
        instance.__dict__[self.name] = value

    def __get__(self, instance: object, owner: any) -> None:
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

    def __set_name__(self, owner: object, name: str) -> None:
        self.name = name


class Visitor:
    age = IntegerRange(0, 120)
    weight = IntegerRange(0, 200)
    height = IntegerRange(0, 250)

    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self._age = age
        self._weight = weight
        self._height = height

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: any) -> None:
        Visitor.age.__set__(self, value)

    @property
    def weight(self) -> int:
        return self._weight

    @weight.setter
    def weight(self, value: any) -> None:
        Visitor.weight.__set__(self, value)

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: any) -> None:
        Visitor.height.__set__(self, value)


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    @abstractmethod
    def validate(self, visitor: object) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            IntegerRange(4, 14),
            IntegerRange(20, 50),
            IntegerRange(80, 120)
        )

    def validate(self, visitor: object) -> list:
        return (
            self.age.__get__(visitor, Visitor)
            and self.weight.__get__(visitor, Visitor)
            and self.height.__get__(visitor, Visitor)
        )

    def can_access(self, visitor: object) -> list:
        return all(
            getattr(visitor, attr) in range(
                getattr(self, attr).min_amount,
                getattr(self, attr).max_amount + 1
            )
            for attr in ("age", "weight", "height")
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            IntegerRange(14, 60),
            IntegerRange(50, 120),
            IntegerRange(120, 220)
        )

    def validate(self, visitor: object) -> list:
        return (
            self.age.__get__(visitor, Visitor)
            and self.weight.__get__(visitor, Visitor)
            and self.height.__get__(visitor, Visitor)
        )

    def can_access(self, visitor: object) -> list:
        return all(
            getattr(visitor, attr) in range(
                getattr(self, attr).min_amount,
                getattr(self, attr).max_amount + 1
            ) for attr in ("age", "weight", "height")
        )


class Slide:
    def __init__(self, name: str, limitation_class: object) -> None:
        self.name = name
        self.limitation = limitation_class()

    def can_access(self, visitor: object) -> bool:
        return self.limitation.can_access(visitor)
