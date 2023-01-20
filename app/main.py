from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.max_amount = max_amount
        self.min_amount = min_amount

    def __set_name__(self, owner, name: str) -> None:
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        if self.min_amount < value < self.max_amount:
            setattr(obj, self.private_name, value)
        else:
            setattr(obj, self.private_name, "")


class Visitor:
    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age, height, weight):
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def __init__(self, age, height, weight):
        super().__init__(age, height, weight)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age, height, weight):
        super().__init__(age, height, weight)


class Slide:
    def __init__(self, name, limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        self.limitation_class.age = visitor.age
        self.limitation_class.height = visitor.height
        self.limitation_class.weight = visitor.weight
        return all(
            (
                1 if self.limitation_class.age else 0,
                1 if self.limitation_class.height else 0,
                1 if self.limitation_class.weight else 0,
            )
        )


v = Visitor("Taras", age=17, weight=67, height=175)

Child = ChildrenSlideLimitationValidator(age=5, weight=30, height=100)
print(Child.__dict__)

Adult = AdultSlideLimitationValidator(age=20, weight=100, height=180)
print(Adult.__dict__)
slide1 = Slide("Horka", Adult)
slide2 = Slide("Horka", Child)
print(slide1.can_access(v))
print(slide2.can_access(v))
