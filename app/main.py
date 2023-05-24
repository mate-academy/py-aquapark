from abc import ABC


class IntegerRange:
    def __init__(self, min_amount, max_amount):
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner, name):
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.protected_name)

    def __set__(self, instance, value):
        print('- - -')

        if self.min_amount <= value <= self.max_amount:
            print('- - -')

            setattr(instance, self.protected_name, value)


class Visitor:

    # age = IntegerRange(4, 14)
    # height = IntegerRange(80, 120)
    # weight = IntegerRange(20, 50)

    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self):
        self._age = 0
        self._height = 0
        self._weight = 0



class AdultSlideLimitationValidator(SlideLimitationValidator):
    pass


class Slide:
    def __init__(self, name, limitation_class):
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor):
        for attr_name, attr_value in vars(visitor).items():
            # print(attr_name)
            if hasattr(self.limitation_class, attr_name):



baby_slide = Slide(name="Baby Slide", limitation_class=ChildrenSlideLimitationValidator)

age = 17
height = 175
weight = 67

visitor = Visitor(name="User", age=age, height=height, weight=weight)

print(baby_slide.can_access(visitor))

# # print(vars(visitor).items())
# # print(ChildrenSlideLimitationValidator.__dict__)
# lim = ChildrenSlideLimitationValidator()
# # attr = "weight"
# # print(lim.__dict__)
# # print(hasattr(lim, "age"))