from abc import ABC


class IntegerRange:

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: object, name: str) -> None:
        self.private_attribute = f"_{name}"

    def __get__(self, instance: object, owner: object) -> bool:
        return getattr(instance, self.private_attribute)

    def __set__(self, instance: object, value: int) -> None:
        if self.max_amount >= value >= self.min_amount:
            setattr(instance, self.private_attribute, True)
        else:
            setattr(instance, self.private_attribute, False)


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

    def __init__(self,
                 name: str,
                 limitation_class: type(SlideLimitationValidator)
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        slide_validate = self.limitation_class(
            age=visitor.age,
            weight=visitor.weight,
            height=visitor.height
        )
        return all(
            [
                slide_validate.weight,
                slide_validate.age,
                slide_validate.height
            ]
        )
