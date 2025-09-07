from abc import ABC


class IntegerRange:
    def __int__(self,
                min_amount: int,
                max_amount: int
                ) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount



class Visitor:
   pass


class SlideLimitationValidator(ABC):
    pass


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    pass


class AdultSlideLimitationValidator(SlideLimitationValidator):
    pass


class Slide:
    pass
