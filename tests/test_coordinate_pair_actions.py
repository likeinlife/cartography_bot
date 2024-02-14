from decimal import Decimal as _

import pytest
from business.math_actions.coordinate_pair_actions import get_delta
from domain.models import Coordinate, CoordinatePair


@pytest.mark.parametrize(
    ("upper_bound", "lower_bound", "parts_number", "expected"),
    [
        (
            CoordinatePair(latitude=Coordinate(degrees=_(10)), longitude=Coordinate(degrees=_(10))),
            CoordinatePair(latitude=Coordinate(degrees=_(5)), longitude=Coordinate(degrees=_(5))),
            2,
            CoordinatePair(
                latitude=Coordinate(degrees=_(2), minutes=_(30)),
                longitude=Coordinate(degrees=_(2), minutes=_(30)),
            ),
        ),
        (
            CoordinatePair(
                latitude=Coordinate(degrees=_(53), minutes=_(15)),
                longitude=Coordinate(degrees=_(47), minutes=_(30)),
            ),
            CoordinatePair(
                latitude=Coordinate(degrees=_(53), minutes=_(10)),
                longitude=Coordinate(degrees=_(47), minutes=_(22), seconds=_(30)),
            ),
            2,
            CoordinatePair(
                latitude=Coordinate(degrees=_(0), minutes=_(2), seconds=_(30)),
                longitude=Coordinate(degrees=_(0), minutes=_(3), seconds=_(45)),
            ),
        ),
    ],
)
def test_get_delta(upper_bound, lower_bound, parts_number, expected):
    assert get_delta(upper_bound, lower_bound, parts_number) == expected
