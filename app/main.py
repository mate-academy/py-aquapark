from abc import ABC


class IntegerRange:
    def __init__(self, min_value: int, max_value: int) -> None:
        if min_value > max_value:
            raise ValueError(
                "Not in range"
            )

        self.min_value = min_value
        self.max_value = max_value

    def __get__(self, obj: any, owner: any) -> int:
        return getattr(obj, self.__name__)

    def __set__(self, obj: any, value: int) -> None:

        if value < self.min_value or value > self.max_value:
            raise ValueError("Not in range")

        setattr(obj, self.__name__, value)


class SlideLimitationValidator(ABC):
    def __init__(self, age_range: IntegerRange,
                 weight_range: IntegerRange,
                 height_range: IntegerRange
                 ) -> None:
        self.age_range = age_range
        self.weight_range = weight_range
        self.height_range = height_range

    def __set__(self, obj: any, value: any) -> None:
        setattr(obj, "__dict__", value)


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age_range=IntegerRange(4, 14),
                         weight_range=IntegerRange(20, 50),
                         height_range=IntegerRange(80, 120))


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age_range=IntegerRange(14, 60),
                         weight_range=IntegerRange(50, 120),
                         height_range=IntegerRange(120, 200))


class Visitor:
    def __init__(self,
                 name: str,
                 age: int,
                 height: int,
                 weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class: SlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: any) -> bool:
        try:
            # Use setattr to set the values of the limitation_class attributes
            setattr(self.limitation_class, "age_range", visitor.age)
            setattr(self.limitation_class, "weight_range", visitor.weight)
            setattr(self.limitation_class, "height_range", visitor.height)
        except ValueError:
            return False

        return True
