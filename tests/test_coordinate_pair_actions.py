from decimal import Decimal as _

import pytest
from business.math_actions.coordinate_pair_actions import get_delta
from domain.models import Coordinate, CoordinatePair

from .coordinates_help import from_tuple


@pytest.mark.parametrize(
    ("upper_bound", "lower_bound", "parts_number", "expected"),
    [
        (
            CoordinatePair(latitude=from_tuple((10, 0, 0)), longitude=from_tuple((10, 0, 0))),
            CoordinatePair(latitude=from_tuple((5, 0, 0)), longitude=from_tuple((5, 0, 0))),
            2,
            CoordinatePair(latitude=from_tuple((2, 30, 0)), longitude=from_tuple((2, 30, 0))),
        ),
        (
            CoordinatePair(latitude=from_tuple((53, 15, 0)), longitude=from_tuple((47, 30, 0))),
            CoordinatePair(latitude=from_tuple((53, 10, 0)), longitude=from_tuple((47, 22, 30))),
            2,
            CoordinatePair(latitude=from_tuple((0, 2, 30)), longitude=from_tuple((0, 3, 45))),
        ),
    ],
)
def test_get_delta(upper_bound, lower_bound, parts_number, expected):
    assert get_delta(upper_bound, lower_bound, parts_number) == expected
