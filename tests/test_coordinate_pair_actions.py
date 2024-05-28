import pytest
from cartography.math_actions.coordinate_pair_actions import get_delta
from domain.models import CoordinatePair
from misc import from_tuple


@pytest.mark.parametrize(
    ("upper_bound", "lower_bound", "parts_number", "expected"),
    [
        (
            CoordinatePair(latitude=from_tuple(10), longitude=from_tuple(10)),
            CoordinatePair(latitude=from_tuple(5), longitude=from_tuple(5)),
            2,
            CoordinatePair(latitude=from_tuple(2, 30), longitude=from_tuple(2, 30)),
        ),
        (
            CoordinatePair(latitude=from_tuple(53, 15), longitude=from_tuple(47, 30)),
            CoordinatePair(latitude=from_tuple(53, 10), longitude=from_tuple(47, 22, 30)),
            2,
            CoordinatePair(latitude=from_tuple(0, 2, 30), longitude=from_tuple(0, 3, 45)),
        ),
    ],
)
def test_get_delta(upper_bound, lower_bound, parts_number, expected):
    assert get_delta(upper_bound, lower_bound, parts_number) == expected
