from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object, owner: type[object]) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.protected_name, value)
        else:
            setattr(instance, self.protected_name, None)

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.protected_name = "_" + name


class Visitor:
    def __init__(self,
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
    @abstractmethod
    def __init__(self, age: int, weight: int, height: int) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self,
                 age: int,
                 weight: int,
                 height: int
                 ) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self,
                 age: int,
                 weight: int,
                 height: int
                 ) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: type[object]
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self,
                   visitor: Visitor
                   ) -> bool:
        new_instance = self.limitation_class(visitor.age,
                                             visitor.weight, visitor.height)
        if new_instance.age is not None \
                and new_instance.weight is not None \
                and new_instance.height is not None:
            return True
        return False
