from abc import ABC


class IntegerRange:
    def __init__(self, min_amount, max_amount):
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner, name):
        self.public = name
        self.protected_name = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("Value should be integer")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError("Value out of range")
        setattr(instance, self.protected_name, value)

class Visitor:
   def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator:
    def __init__(self, age, weight, height):
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
    def __init__(self, name, limitation_class : ChildrenSlideLimitationValidator | AdultSlideLimitationValidator):
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor : Visitor):
        try:
            self.limitation_class(
                age= visitor.age,
                weight= visitor.weight,
                height= visitor.height
            )
            return True
        except (ValueError, TypeError):
            return False