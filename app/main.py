from abc import ABC
from typing import Optional, Type


class IntegerRange:
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(
            self,
            instance: Optional["Visitor"],
            owner: type
    ) -> Optional[int]:
        return getattr(instance, self.protected_name, None)

    def __set__(self, instance: "Visitor", value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        if not (self.min_value <= value <= self.max_value):
            raise ValueError
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: IntegerRange,
            weight: IntegerRange,
            height: IntegerRange
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            age=IntegerRange(4, 14),
            height=IntegerRange(80, 120),
            weight=IntegerRange(20, 50),
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            age=IntegerRange(14, 60),
            height=IntegerRange(120, 220),
            weight=IntegerRange(50, 120)
        )


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: Type[SlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        limitation = self.limitation_class()

        if not (limitation.age.min_value
                <= visitor.age
                <= limitation.age.max_value):
            return False
        if not (limitation.weight.min_value
                <= visitor.weight
                <= limitation.weight.max_value):
            return False
        if not (limitation.height.min_value
                <= visitor.height
                <= limitation.height.max_value):
            return False

        return True
