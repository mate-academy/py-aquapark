from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: object, owner: object) -> int:
        return getattr(instance, self._name)

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("Value must be an integer")
        if not self.min_amount <= value <= self.max_amount:
            raise ValueError(f"Value must be between {self.min_amount}"
                             f" and {self.max_amount}")
        setattr(instance, self._name, value)

    def __set_name__(self, owner: object, name: str) -> None:
        self._name = name


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: IntegerRange(int, int),
            weight: IntegerRange(int, int),
            height: IntegerRange(int, int)
    ) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            IntegerRange(4, 14),
            IntegerRange(20, 50),
            IntegerRange(80, 120)
        )

    def validate(self, visitor: Visitor) -> bool:
        return all([
            self.age.min_amount <= visitor.age <= self.age.max_amount,
            self.weight.min_amount <= visitor.weight <= self.weight.max_amount,
            self.height.min_amount <= visitor.height <= self.height.max_amount
        ])


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            IntegerRange(14, 60),
            IntegerRange(50, 120),
            IntegerRange(120, 220)
        )

    def validate(self, visitor: Visitor) -> bool:
        return all([
            self.age.min_amount <= visitor.age <= self.age.max_amount,
            self.weight.min_amount <= visitor.weight <= self.weight.max_amount,
            self.height.min_amount <= visitor.height <= self.height.max_amount
        ])


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_validator = None
        try:
            self.limitation_validator = limitation_class()
        except Exception as e:
            print(f"Error initializing limitation validator: {e}")

    def can_access(self, visitor: Visitor) -> bool:
        if self.limitation_validator:
            return self.limitation_validator.validate(visitor)
        return False
