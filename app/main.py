from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance, owner) -> bool:
        if self.min_amount < instance < self.max_amount:
            return instance

    def __set__(self, instance, value):
        self.min_amount = instance.min_amount
        self.max_amount = instance.max_amount

    def __set_name__(self, owner, name):
        # self.name = owner.name
        pass


class Visitor:

    def __init__(self, name: int, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    age_range: IntegerRange
    weight_range: IntegerRange
    height_range: IntegerRange

    def __init__(self, age, weight, height) -> None:
        self.age = age
        self.weight = weight
        self.height = height

    def __get__(self, instance, owner) -> None:
        pass

    def __set__(self, instance, value) -> None:
        pass

    def __set_name__(self, owner, name) -> None:
        pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age_range = IntegerRange(4, 14)
    weight_range = IntegerRange(80, 120)
    height_range = IntegerRange(20, 50)

    def __init__(self, age, weight, height) -> None:
        super().__init__(age, weight, height)

    def __get__(self, instance, owner) -> None:



class AdultSlideLimitationValidator(SlideLimitationValidator):
    age_range = IntegerRange(14, 60)
    weight_range = IntegerRange(120, 220)
    height_range = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)
        if 14 <= age <= 60:
            self.age = age
        if 120 <= weight <= 220:
            self.weight = weight
        if 50 <= height <= 120:
            self.height = height


class Slide:
    def __init__(self, name: str, limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> str:
        yyy = self.limitation_class

        return "has_access"


# age = 17
# height = 175
# weight = 67

baby_slide = Slide(
        name="Baby Slide", limitation_class=ChildrenSlideLimitationValidator
    )

visitor = Visitor("User", 17, 175, 67)
baby_slide.can_access(visitor) # == has_access

ttt = 0