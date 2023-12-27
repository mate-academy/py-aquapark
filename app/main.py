from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> int:
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.protected_name = None

    def __get__(self, instance: any, owner: any) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: any, value: int) -> None:
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(f"""Value must be between {self.min_amount} and
{self.max_amount}""")
        setattr(instance, self.protected_name, value)

    def __set_name__(self, owner: any, name: str) -> None:
        self.protected_name = f"_{name}"


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age_range: int,
                 height_range: int,
                 weight_range: int) -> int:
        self.age_range = age_range
        self.height_range = height_range
        self.weight_range = weight_range


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age_range=(4, 14),
                         height_range=(80, 120),
                         weight_range=(20, 50))

    def validate(self, visitor: Visitor) -> bool:
        return (self.age_range[0] <= visitor.age <= self.age_range[1]
                and self.height_range[0] <= visitor.height
                <= self.height_range[1]
                and self.weight_range[0] <= visitor.weight
                <= self.weight_range[1])


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(age_range=(14, 60),
                         height_range=(120, 220),
                         weight_range=(50, 120))

    def validate(self, visitor: Visitor) -> bool:
        return (self.age_range[0] <= visitor.age <= self.age_range[1]
                and self.height_range[0] <= visitor.height
                <= self.height_range[1]
                and self.weight_range[0] <= visitor.weight
                <= self.weight_range[1])


class Slide:
    def __init__(self, name: str,
                 limitation_class: SlideLimitationValidator
                 ) -> None:
        self.limitation_validator = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        return self.limitation_validator.validate(visitor)
