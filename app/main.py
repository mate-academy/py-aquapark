from abc import ABC


class IntegerRange:
    def __init__(self, min_amount , max_amount ):
        self.min_amount  = min_amount
        self.max_amount  = max_amount

    def __set_name__(self, owner, name):
        self.name = name  # e.g. "height", "weight", "age"
        self.private = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.private, None)

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(
                f"{self.name} must be an integer, got {type(value).__name__}"
            )
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(
                f"{self.name} must be between {self.min_amount} and {self.max_amount}"
            )
        setattr(instance, self.private, value)

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
