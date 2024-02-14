from decimal import Decimal as _

import pytest
from business.math_actions.coordinate_actions import between, divide, get_middle, minus, multiply, plus
from domain.models import Coordinate

from .coordinates_help import from_tuple


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        (
            from_tuple((10, 10, 10)),
            from_tuple((10, 10, 10)),
            from_tuple((20, 20, 20)),
        ),
        (
            from_tuple((10, 10, 10)),
            from_tuple((10, 50, 10)),
            from_tuple((21, 0, 20)),
        ),
    ],
)
def test_plus(first, second, expected):
    assert plus(first, second) == expected


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        (
            from_tuple((10, 10, 10)),
            from_tuple((10, 10, 10)),
            from_tuple((0, 0, 0)),
        ),
        (
            from_tuple((10, 10, 10)),
            from_tuple((10, 50, 10)),
            from_tuple((0, -40, 0)),
        ),
    ],
)
def test_minus(first, second, expected):
    assert minus(first, second) == expected


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        (
            from_tuple((10, 10, 10)),
            2,
            from_tuple((20, 20, 20)),
        ),
        (
            from_tuple((10, 10, 10)),
            7,
            from_tuple((71, 11, 10)),
        ),
    ],
)
def test_multiply(first, second, expected):
    assert multiply(first, second) == expected


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        (
            from_tuple((10, 10, 10)),
            2,
            from_tuple((5, 5, 5)),
        ),
        (
            from_tuple((10, 10, 10)),
            7,
            from_tuple((1, 27, 10)),
        ),
    ],
)
def test_divide(first, second, expected):
    assert divide(first, second) == expected


@pytest.mark.parametrize(
    "left, this, right, expected",
    [
        (
            from_tuple((10, 10, 10)),
            from_tuple((11, 10, 10)),
            from_tuple((12, 10, 10)),
            True,
        ),
        (
            from_tuple((10, 10, 10)),
            from_tuple((9, 10, 10)),
            from_tuple((12, 10, 10)),
            False,
        ),
    ],
)
def test_between(left, this, right, expected):
    assert between(left, this, right) == expected
