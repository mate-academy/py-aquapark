class IntegerRange:
    def __init__(self, min_amount, max_amount):
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.name = None

    def __set_name__(self, owner, name):
        # We store the value in a private attribute (e.g., _age) 
        # to avoid recursion when setting the value.
        self.name = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        # Retrieve the value from the instance dictionary
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        # 1. Check type
        if not isinstance(value, int):
            raise TypeError("Value must be an integer.")

        # 2. Check range
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"Value {value} is out of range {self.min_amount}-{self.max_amount}.")

        # 3. Store value
        instance.__dict__[self.name] = value


class Visitor:
    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator:
    def __init__(self, age, weight, height):
        # When these are assigned, the Descriptor's __set__ method is triggered
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
    def __init__(self, name, limitation_class):
        self.name = name
        # We store the class itself, not an instance
        self.limitation_class = limitation_class

    def can_access(self, visitor):
        try:
            # We attempt to instantiate the validator.
            # If the visitor's attributes are outside the IntegerRange, 
            # the descriptor in __init__ will raise ValueError or TypeError.
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except (ValueError, TypeError):
            return False
