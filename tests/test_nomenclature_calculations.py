import pytest
from business.calculate_nomenclature import get_1m_nomenclature
from domain.models import CoordinatePair, Nomenclature

from .coordinates_help import from_tuple


@pytest.mark.parametrize(
    "coordinate_pair, expected",
    [
        (
            CoordinatePair(
                latitude=from_tuple(35),
                longitude=from_tuple(3),
            ),
            Nomenclature(
                title="I-31",
                lower_bound=CoordinatePair(
                    latitude=from_tuple(32),
                    longitude=from_tuple(0),
                ),
                upper_bound=CoordinatePair(
                    latitude=from_tuple(36),
                    longitude=from_tuple(6),
                ),
            ),
        )
    ],
)
def test_get_1m_nomenclature(coordinate_pair, expected):
    assert get_1m_nomenclature(coordinate_pair) == expected


# @pytest.mark.parametrize(
#     "coordinate_pair, parts_number, previous_nomenclature, alphabet, title_formatter, expected",
#     [(from_tuple(()))],
# )
# def test_get_nomenclature_by_parts(coordinate_pair, expected):
#     assert get_1m_nomenclature(coordinate_pair) == expected
