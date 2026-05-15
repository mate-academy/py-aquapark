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
    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height

    def __repr__(self):
        return (
            f"Visitor(name={self.name!r}, age={self.age}, "
            f"weight={self.weight} kg, height={self.height} cm)"
        )


class SlideLimitationValidator(ABC):
    def __init__(self, age, weight, height):
        self.age    = age
        self.weight = weight
        self.height = height

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.age    = visitor.age
            self.weight = visitor.weight
            self.height = visitor.height
            return True
        except (TypeError, ValueError):
            return False


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)

    def __init__(self):
        super().__init__(age=4, weight=20, height=80)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)

    def __init__(self):
        super().__init__(age=14, weight=50, height=120)


class Slide:
    def __init__(self, name, limitation_class):
        self.name       = name
        self.limitation = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation.can_access(visitor)
