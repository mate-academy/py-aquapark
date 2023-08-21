from abc import ABC


class IntegerRange:

    def __init__(
            self,
            min_amount: int,
            max_amount: int
    ) -> None:

        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: object, name: str) -> None:
        self.private_name = "_" + name
        print(owner)

    def __get__(self, instance: object, owner: object) -> float:
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: float) -> float | None:
        if self.min_amount <= value <= self.max_amount:
            return setattr(instance, self.private_name, value)
        print(f"Value must be"
              f"{self.min_amount}...{self.max_amount}")
        return setattr(instance, self.private_name, None)


class Visitor:

    def __init__(
            self,
            name: str,
            age: int | None,
            weight: float | None,
            height: float | None) -> None:

        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):

    def __init__(
            self,
            name: str,
            age: int | None,
            weight: float | None,
            height: float | None) -> None:

        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(min_amount=4, max_amount=14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):

    age = IntegerRange(min_amount=14, max_amount=60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:

    def __init__(
            self,
            name: str,
            limitation_class: AdultSlideLimitationValidator
            | ChildrenSlideLimitationValidator
    ) -> None:

        self.limitation_class = limitation_class
        self.name = name

    def can_access(self, visitor: Visitor) -> bool:
        instance = self.limitation_class(visitor.name,
                                         visitor.age,
                                         visitor.weight,
                                         visitor.height)

        if (instance.age
                is None or instance.height
                is None or instance.weight
                is None):
            return False
        return True
