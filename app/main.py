class IntegerRangeClasse:
    def __init__(self, min_amount, max_amount):
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.name = None

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name, None)

    def validate(self, value):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("O valor deve ser um número inteiro.")
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"O valor deve estar entre {self.min_amount} e {self.max_amount}.")

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.name, value)


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
    age = IntegerRangeClasse(4, 14)
    height = IntegerRangeClasse(80, 120)
    weight = IntegerRangeClasse(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRangeClasse(14, 60)
    height = IntegerRangeClasse(120, 220)
    weight = IntegerRangeClasse(50, 120)


class Slide:
    def __init__(self, name, limitation_class):
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor):
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except (ValueError, TypeError):
            return False
