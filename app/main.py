from abc import ABC


class IntegerRange:
    def __init__(
            self,
            min_amount: int,
            max_amount: int
    ) -> None:
        self._min_amount = min_amount
        self._max_amount = max_amount

    def __set_name__(
            self,
            owner: type["SlideLimitationValidator"],
            name: str
    ) -> None:
        self.private_name = "_" + name

    def __get__(
            self,
            obj: type["SlideLimitationValidator"],
            objtype: None
    ) -> int:
        getattr(obj, self.private_name)

    def __set__(
            self,
            obj: type["SlideLimitationValidator"],
            value: int
    ) -> None:
        if value not in range(self._min_amount, self._max_amount + 1):
            raise ValueError(
                f"The value should be not less than {self._min_amount} "
                f"and not greater than {self._max_amount}."
            )
        setattr(obj, self.private_name, value)


class SlideLimitationValidator(ABC):
    def __init__(
            self,
            age: int,
            weight: int,
            height: int
    ) -> None:
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


class Visitor(SlideLimitationValidator):
    def __init__(
            self,
            name: str,
            age: int,
            weight: int,
            height: int
    ) -> None:
        self.name = name
        super().__init__(age, weight, height)


class Slide:
    def __init__(
            self,
            name: str,
            limitation_class: SlideLimitationValidator
    ) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
        except ValueError:
            print(f"{visitor.name} can't use {self.name}")
            return False
        return True
