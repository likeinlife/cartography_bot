import pytest
from business.scale_resolver import coordinate_resolver
from domain.enums import Scale
from domain.models import CoordinatePair, Nomenclature
from misc import from_tuple

from .test_helper import generate_random_bound


@pytest.mark.parametrize(
    "coordinate_pair, scale, expected",
    [
        (
            CoordinatePair(
                latitude=from_tuple(35),
                longitude=from_tuple(3),
            ),
            1,
            {
                Scale._1M: Nomenclature(
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
            },
        )
    ],
)
def test_1m(coordinate_pair, scale, expected):
    chain_link = coordinate_resolver.get_scale(scale)
    assert chain_link.resolve(coordinate_pair) == expected


@pytest.mark.parametrize(
    "coordinate_pair, scale, expected",
    [
        (
            CoordinatePair(
                latitude=from_tuple(51),
                longitude=from_tuple(65),
            ),
            2,
            {
                Scale._1M: Nomenclature(
                    title="M-41",
                    lower_bound=CoordinatePair(
                        latitude=from_tuple(48),
                        longitude=from_tuple(60),
                    ),
                    upper_bound=CoordinatePair(
                        latitude=from_tuple(52),
                        longitude=from_tuple(66),
                    ),
                    outer_lower_bound=generate_random_bound(),
                    outer_upper_bound=generate_random_bound(),
                ),
                Scale._500K: Nomenclature(
                    title="M-41-Б",
                    lower_bound=CoordinatePair(
                        latitude=from_tuple(50),
                        longitude=from_tuple(63),
                    ),
                    upper_bound=CoordinatePair(
                        latitude=from_tuple(52),
                        longitude=from_tuple(66),
                    ),
                    cell_to_fill="Б",
                    outer_lower_bound=CoordinatePair(
                        latitude=from_tuple(48),
                        longitude=from_tuple(60),
                    ),
                    outer_upper_bound=CoordinatePair(
                        latitude=from_tuple(52),
                        longitude=from_tuple(66),
                    ),
                ),
            },
        )
    ],
)
def test_500k(coordinate_pair, scale, expected):
    chain_link = coordinate_resolver.get_scale(scale)
    assert chain_link.resolve(coordinate_pair) == expected


@pytest.mark.parametrize(
    "coordinate_pair, scale, expected",
    [
        (
            CoordinatePair(
                latitude=from_tuple(51),
                longitude=from_tuple(65),
            ),
            3,
            {
                Scale._1M: Nomenclature(
                    title="M-41",
                    lower_bound=CoordinatePair(
                        latitude=from_tuple(48),
                        longitude=from_tuple(60),
                    ),
                    upper_bound=CoordinatePair(
                        latitude=from_tuple(52),
                        longitude=from_tuple(66),
                    ),
                    outer_lower_bound=generate_random_bound(),
                    outer_upper_bound=generate_random_bound(),
                ),
                Scale._500K: Nomenclature(
                    title="M-41-Б",
                    lower_bound=CoordinatePair(
                        latitude=from_tuple(50),
                        longitude=from_tuple(63),
                    ),
                    upper_bound=CoordinatePair(
                        latitude=from_tuple(52),
                        longitude=from_tuple(66),
                    ),
                    cell_to_fill="Б",
                    outer_lower_bound=CoordinatePair(
                        latitude=from_tuple(48),
                        longitude=from_tuple(60),
                    ),
                    outer_upper_bound=CoordinatePair(
                        latitude=from_tuple(52),
                        longitude=from_tuple(66),
                    ),
                ),
                Scale._300K: Nomenclature(
                    title="III-M-41",
                    lower_bound=CoordinatePair(
                        latitude=from_tuple(50, 40),
                        longitude=from_tuple(64),
                    ),
                    upper_bound=CoordinatePair(
                        latitude=from_tuple(52),
                        longitude=from_tuple(66),
                    ),
                    cell_to_fill="III",
                    outer_lower_bound=CoordinatePair(
                        latitude=from_tuple(48),
                        longitude=from_tuple(60),
                    ),
                    outer_upper_bound=CoordinatePair(
                        latitude=from_tuple(52),
                        longitude=from_tuple(66),
                    ),
                ),
            },
        )
    ],
)
def test_300k(coordinate_pair, scale, expected):
    chain_link = coordinate_resolver.get_scale(scale)
    assert chain_link.resolve(coordinate_pair) == expected
