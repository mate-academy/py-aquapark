from abc import ABC


class IntegerRange:

    def __set_name__(self, owner: any, name: str) -> None:
        self.protected_name = "_" + name

    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: any, owner: any) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: any, value: any) -> None:
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self, age: IntegerRange,
                 weight: IntegerRange,
                 height: IntegerRange) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age=IntegerRange(4, 14),
                         weight=IntegerRange(20, 50),
                         height=IntegerRange(80, 120))


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age=IntegerRange(14, 60),
                         weight=IntegerRange(50, 120),
                         height=IntegerRange(120, 220))


class Slide:
    def __init__(self, name: str,
                 limitation_class: SlideLimitationValidator
                 ) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def __age_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.age.min_amount \
            <= visitor.age <= \
            self.limitation_class.age.max_amount

    def __weight_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.weight.min_amount\
            <= visitor.weight <= \
            self.limitation_class.weight.max_amount

    def __height_access(self, visitor: Visitor) -> bool:
        return self.limitation_class.height.min_amount \
            <= visitor.height <= \
            self.limitation_class.height.max_amount

    def can_access(self, visitor: Visitor) -> bool:
        return self.__age_access(visitor) \
            and self.__weight_access(visitor) \
            and self.__height_access(visitor)
