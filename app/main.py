from abc import ABC


class IntegerRange:

    def __init__(self,
                 min_amount: int,
                 max_amount: int) -> None:

        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, obj: any, name: str) -> None:
        self._name = "_" + name

    def __get__(self, obj: any, owner: any) -> int:
        return getattr(obj, self._name)

    def __set__(self, obj: any, value: int) -> None:

        if not self.min_amount <= value <= self.max_amount:
            raise ValueError("Not in range")

        setattr(obj, self._name, value)


class Visitor:

    def __init(self,
               name: str,
               age: int,
               weight: int,
               height: int) -> None:

        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):

    def __int__(self,
                age_integer: IntegerRange,
                weight_integer: IntegerRange,
                height_integer: IntegerRange
                ) -> None:

        self.age = age_integer
        self.weight = weight_integer
        self.height = height_integer


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age_integer=IntegerRange(4, 14),
                         weight_integer=IntegerRange(20, 50),
                         height_integer=IntegerRange(80, 120))


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age_integer=IntegerRange(14, 60),
                         weight_integer=IntegerRange(50, 120),
                         height_integer=IntegerRange(120, 220))


class Slide:

    def __init__(self,
                 name: str,
                 limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:

        try:
            visitor.age = self.limitation_class.age
            visitor.weight = self.limitation_class.weight
            visitor.height = self.limitation_class.height

        except ValueError:
            return False

        return True
