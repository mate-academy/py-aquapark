from abc import ABC


class IntegerRange:

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(
            self,
            instance: "SlideLimitationValidator",
            owner: type
    ) -> int:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(
            self,
            instance: "SlideLimitationValidator",
            value: int
    ) -> None:
        setattr(instance, self.protected_name, None)
        if self.min_amount <= value <= self.max_amount:
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
            self, name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        obj = self.limitation_class(
            age=visitor.age,
            height=visitor.height,
            weight=visitor.weight
        )
        return all([obj.age, obj.height, obj.weight])


if __name__ == "__main__":

    adult_slide = Slide("adult", AdultSlideLimitationValidator)
    baby_slide = Slide("baby", ChildrenSlideLimitationValidator)

    anna = Visitor(
        name="Anna",
        age=11,
        weight=50,
        height=165
    )

    print(adult_slide.limitation_class.age)

    print(adult_slide.name)
    print(baby_slide.name)
    print(anna.name, "\n", anna.age, "\n", anna.height, "\n", anna.weight)
    print(adult_slide.can_access(anna))
