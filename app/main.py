from abc import ABC


class IntegerRange:
    def __init__(self, name: str, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self._value = None

    def __set_name__(self, owner: any, name: str) -> None:
        self._protected_name = "_" + name
        pass

    def __get__(self, obj: any = None) -> int:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: any, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Wrong value type")
        elif not self.is_value_in_range(value):
            raise ValueError("Value not in range")
        else:
            setattr(obj, self._protected_name, value)

    def is_value_in_range(self, value: int) -> bool:
        return self.max_amount >= value >= self.min_amount


class Visitor:
    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange("age", 4, 14)
    height = IntegerRange("height", 80, 120)
    weight = IntegerRange("weight", 20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange("age", 14, 60)
    height = IntegerRange("height", 120, 220)
    weight = IntegerRange("weight", 50, 120)


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.height, visitor.weight)
            return True
        except (TypeError, ValueError):
            return False
