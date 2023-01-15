from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: object, name: str) -> None:
        self.name = "_" + name

    def __set__(self, instance: object, value: int) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.name, True)
        else:
            setattr(instance, self.name, False)

    def __get__(self, instance: object, owner: object) -> getattr:
        return getattr(instance, self.name)


class Visitor:
    def __init__(
            self,
            name: str,
            age: int,
            height: int,
            weight: int
    ) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            weight: int,
            age: int,
            height: int
    ) -> None:
        self.weight = weight
        self.age = age
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(
            self,
            age: int,
            height: int,
            weight: int
    ) -> None:
        super().__init__(age, height, weight)
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
            weight: int
    ) -> None:
        super().__init__(age, height, weight)
        self.age = age
        self.height = height
        self.weight = weight


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: [ChildrenSlideLimitationValidator,
                               AdultSlideLimitationValidator]
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        validate = self.limitation_class(visitor.age,
                                         visitor.height,
                                         visitor.weight)
        return all([validate.age,
                    validate.height,
                    validate.weight])
