import pytest
from domain.models import CoordinatePair, Nomenclature
from logic.cartography.calculations.coordinates import get_1m_nomenclature, get_nomenclature_by_parts
from logic.cartography.constants import UPPER_ALPHA
from misc import from_tuple

from .test_helper import generate_random_bound


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
                outer_lower_bound=generate_random_bound(),
                outer_upper_bound=generate_random_bound(),
            ),
        )
    ],
)
def test_get_1m_nomenclature(coordinate_pair, expected):
    assert get_1m_nomenclature(coordinate_pair) == expected


@pytest.mark.parametrize(
    "coordinate_pair, parts_number, previous_nomenclature, alphabet, title_formatter, expected",
    [
        (
            CoordinatePair(
                latitude=from_tuple(14, 59, 8),
                longitude=from_tuple(148, 14, 22),
            ),
            2,
            Nomenclature(
                title="D-55",
                lower_bound=CoordinatePair(
                    latitude=from_tuple(12),
                    longitude=from_tuple(144),
                ),
                upper_bound=CoordinatePair(
                    latitude=from_tuple(16),
                    longitude=from_tuple(150),
                ),
                outer_lower_bound=generate_random_bound(),
                outer_upper_bound=generate_random_bound(),
            ),
            UPPER_ALPHA,
            lambda x, y: f"{x}-{y}",
            Nomenclature(
                title="D-55-Б",
                lower_bound=CoordinatePair(
                    latitude=from_tuple(14),
                    longitude=from_tuple(147),
                ),
                upper_bound=CoordinatePair(
                    latitude=from_tuple(16),
                    longitude=from_tuple(150),
                ),
                cell_to_fill="Б",
                outer_lower_bound=CoordinatePair(
                    latitude=from_tuple(12),
                    longitude=from_tuple(144),
                ),
                outer_upper_bound=CoordinatePair(
                    latitude=from_tuple(16),
                    longitude=from_tuple(150),
                ),
            ),
        )
    ],
)
def test_get_nomenclature_by_parts(
    coordinate_pair, parts_number, previous_nomenclature, alphabet, title_formatter, expected
):
    assert (
        get_nomenclature_by_parts(
            coordinate_pair,
            parts_number,
            previous_nomenclature,
            alphabet,
            title_formatter,
        )
        == expected
    )
