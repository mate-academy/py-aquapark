from abc import ABC


class IntegerRange:
    def __init__(
        self,
        min_range: int,
        max_range: int,
    ) -> None:
        self.min_range = min_range
        self.max_range = max_range

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.private_name = "_" + name

    def __get__(self, instance: object, owner: type = None) -> int:
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: int) -> None:
        if not self.min_range <= value <= self.max_range:
            raise ValueError(
                "Value must be in range: "
                f"{self.min_range} ... {self.max_range}"
            )
        setattr(instance, self.private_name, value)


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
    def __init__(
        self,
        age: int,
        weight: int,
        height: int,
    ) -> None:
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
        limitation_class: type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(
                visitor.age,
                visitor.weight,
                visitor.height,
            )
            return True
        except ValueError:
            print("Access denied")
            return False
