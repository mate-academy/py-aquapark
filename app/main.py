from abc import ABC


class IntegerRange:
    def __init__(self, min_amount, max_amount):
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if self.min_amount <= value <= self.max_amount:
            setattr(instance, self.name, value)
        else:
            raise ValueError(f"Value {value} is out of range "
                             f"from {self.min_amount} to {self.max_amount}")

    def __set_name__(self, owner, name):
        self.name = name





class Visitor:
   pass


class SlideLimitationValidator(ABC):
    pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    pass


class AdultSlideLimitationValidator(SlideLimitationValidator):
    pass


class Slide:
    pass


tteesstt = IntegerRange(1,100)
tteesstt.__set__(IntegerRange,101)