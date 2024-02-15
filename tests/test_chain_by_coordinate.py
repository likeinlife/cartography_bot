import pytest
from business.chain import coordinate_chain
from domain.enums import Scale
from domain.models import CoordinatePair, Nomenclature
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
def test_1m(coordinate_pair, expected):
    assert coordinate_chain.ChainLink1M.resolve(coordinate_pair) == expected


@pytest.mark.parametrize(
    "coordinate_pair, expected",
    [
        (
            CoordinatePair(
                latitude=from_tuple(51),
                longitude=from_tuple(65),
            ),
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
def test_500k(coordinate_pair, expected):
    assert coordinate_chain.ChainLink500K.resolve(coordinate_pair) == expected


@pytest.mark.parametrize(
    "coordinate_pair, expected",
    [
        (
            CoordinatePair(
                latitude=from_tuple(51),
                longitude=from_tuple(65),
            ),
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
def test_300k(coordinate_pair, expected):
    assert coordinate_chain.ChainLink300K.resolve(coordinate_pair) == expected
