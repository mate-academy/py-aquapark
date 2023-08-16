from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, max_amount: int, min_amount: int) -> None:
        self.name = None
        self.max_amount = max_amount
        self.min_amount = min_amount

    def __get__(self, instance: None, owner: None) -> None:
        return getattr(instance, f"_{self.name}")

    def __set_name__(self, owner: None, name: None) -> None:
        self.name = name

    def __set__(self, instance: None, value: int) -> None:
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, f"_{self.name}", value)
        else:
            raise ValueError(f"{self.name.capitalize()} should be between "
                             f"{self.min_amount} and {self.max_amount}")


class Visitor:
    def __init__(self, name: str, age: int,
                 weight: int, height: int) -> None:
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
    def can_use_slide(self) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator, ABC):
    def can_use_slide(self) -> bool:
        if 4 <= self.age <= 14 and 80 <= self.height\
                <= 120 and 20 <= self.weight <= 50:
            return True
        return False


class AdultSlideLimitationValidator(SlideLimitationValidator, ABC):
    def can_use_slide(self) -> bool:
        if 14 <= self.age <= 60 and 220 >= self.height \
                >= 120 >= self.weight >= 50:
            return True
        return False


class Slide:
    def __init__(self, name: str, limitation_class: None) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: any) -> None:
        return self.limitation_class(visitor.age, visitor.weight,
                                     visitor.height).can_use_slide()
