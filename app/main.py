from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: any, name: str) -> None:
        self.name = name
        self.protected_name = "_" + name

    def __get__(self, instance, owner: any) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance, value: str | int) -> None:
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(
                f"{self.name} must be in range from {self.min_amount} to {self.max_amount}"
            )
        setattr(instance, self.protected_name, value)


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

    @abstractmethod
    def can_access(self, instance: Visitor) -> any:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)

    def can_access(self, instance: Visitor) -> any:
        return instance


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)

    def can_access(self, instance: Visitor) -> any:
        return instance


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: ChildrenSlideLimitationValidator | AdultSlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> any:
        return self.limitation_class.can_access(visitor)



