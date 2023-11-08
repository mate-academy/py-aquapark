from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: any, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, obj: any, objtype: any = None) -> any:
        value = getattr(obj, self.protected_name)
        return value

    def __set__(self, obj: any, value: int) -> None:
        setattr(obj, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)

#    age = IntegerRange(4, 14)
#    weight = IntegerRange(20, 50)
#    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class:
            ChildrenSlideLimitationValidator | AdultSlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        if (self.limitation_class.__name__
                == "ChildrenSlideLimitationValidator"):
            if (4 <= visitor.age <= 14
                    and 80 <= visitor.height <= 120
                    and 20 <= visitor.weight <= 50):
                return True
            return False

        if (14 <= visitor.age <= 60
                and 220 >= visitor.height >= 120 >= visitor.weight >= 50):
            return True
        return False
