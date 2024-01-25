import pytest
from app.main import (
    Visitor,
    ChildrenSlideLimitationValidator,
    AdultSlideLimitationValidator,
    Slide,
)


@pytest.mark.parametrize(
    "age,height,weight,has_access",
    (
        pytest.param(17, 175, 67, False, id="failed-for-adult"),
        pytest.param(3, 100, 25, False, id="failed-if-age-less-than-4"),
        pytest.param(5, 70, 25, False, id="failed-if-height-less-than-80"),
        pytest.param(5, 90, 15, False, id="failed-if-weight-less-than-20"),
        pytest.param(15, 100, 25, False, id="failed-if-age-greater-than-14"),
        pytest.param(5, 130, 25, False, id="failed-if-height-greater-than-120"),
        pytest.param(5, 100, 55, False, id="failed-if-weight-greater-than-50"),
        pytest.param(10, 120, 30, True, id="success"),
        pytest.param(4, 80, 20, True, id="success-for-min-accessible-values"),
        pytest.param(14, 120, 50, True, id="success-for-max-accessible-values"),
    )
)
def test_child_slide(age: int, height: int, weight: int, has_access: bool) -> None:
    baby_slide = Slide(
        name="Baby Slide", limitation_class=ChildrenSlideLimitationValidator
    )
    visitor = Visitor(name="User", age=age, height=height, weight=weight)
    assert (
        baby_slide.can_access(visitor) == has_access
    ), (
        f"Baby-slide 'can_access' method should return '{has_access}' for visitor with such parameters: (age: {age}, "
        f"weight: {weight}, height: {height}). But actual result is {baby_slide.can_access(visitor)}"
    )


@pytest.mark.parametrize(
    "age,height,weight,has_access",
    (
        pytest.param(13, 160, 60, False, id="failed-if-age-less-than-14"),
        pytest.param(14, 70, 50, False, id="failed-if-height-less-than-120"),
        pytest.param(25, 150, 45, False, id="failed-if-weight-less-than-50"),
        pytest.param(70, 160, 65, False, id="failed-if-age-greater-than-60"),
        pytest.param(25, 230, 80, False, id="failed-if-height-greater-than-220"),
        pytest.param(25, 160, 135, False, id="failed-if-weight-greater-than-120"),
        pytest.param(25, 160, 60, True, id="success"),
        pytest.param(14, 120, 50, True, id="success-for-min-accessible-values"),
        pytest.param(60, 220, 120, True, id="success-for-max-accessible-values"),
    )
)
def test_adult_slide(age: int, height: int, weight: int, has_access: bool) -> None:
    adult_slide = Slide(
        name="Adult Slide", limitation_class=AdultSlideLimitationValidator
    )
    visitor = Visitor(name="User", age=age, height=height, weight=weight)
    assert (
        adult_slide.can_access(visitor) == has_access
    ), (
        f"Adult-slide 'can_access' method should return '{has_access}' for visitor with such parameters: (age: {age}, "
        f"weight: {weight}, height: {height}). But actual result is {adult_slide.can_access(visitor)}"
    )
