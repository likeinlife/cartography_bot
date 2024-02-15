import pytest
from business.chain import coordinate_chain
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
            {
                "1m": Nomenclature(
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
                "1m": Nomenclature(
                    title="M-41",
                    lower_bound=CoordinatePair(
                        latitude=from_tuple(48),
                        longitude=from_tuple(60),
                    ),
                    upper_bound=CoordinatePair(
                        latitude=from_tuple(52),
                        longitude=from_tuple(66),
                    ),
                ),
                "500k": Nomenclature(
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
                "1m": Nomenclature(
                    title="M-41",
                    lower_bound=CoordinatePair(
                        latitude=from_tuple(48),
                        longitude=from_tuple(60),
                    ),
                    upper_bound=CoordinatePair(
                        latitude=from_tuple(52),
                        longitude=from_tuple(66),
                    ),
                ),
                "500k": Nomenclature(
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
                ),
                "300k": Nomenclature(
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
                ),
            },
        )
    ],
)
def test_300k(coordinate_pair, expected):
    assert coordinate_chain.ChainLink300K.resolve(coordinate_pair) == expected
