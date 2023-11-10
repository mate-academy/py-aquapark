from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        return getattr(instance, self._name)

    def __set__(self, instance, value):
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"Value must be between {self.min_amount} and {self.max_amount}")
        setattr(instance, self._name, value)



class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height

# 2. Visitor класс, отвечающий за персональные данные пользователя
# Его __init__ метод принимает name, age, weight, и height.


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height



# 3. SlideLimitationValidator класс, унаследованный от ABC класса
# Его __init__метод принимает age, weight, и height.


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(self,name: str, limitation_class):
        self.name = name
        self.limitation_class = limitation_class


    def can_access(self, visit: Visitor):
        try:
            self.limitation_class(visit.age, visit.weight, visit.height)
            return True
        except ValueError:
            return False