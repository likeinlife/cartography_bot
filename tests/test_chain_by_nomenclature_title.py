import pytest
from business.enums import Scale
from business.models import CoordinatePair, Nomenclature
from business.scale_resolver import nomenclature_title_resolver
from misc import from_tuple

from .test_helper import generate_random_bound


@pytest.mark.parametrize(
    "nomenclature_title, expected",
    [
        (
            "I-31",
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
def test_1m(nomenclature_title, expected):
    chain_link, nomenclature_title_dict = nomenclature_title_resolver.parse_nomenclature_string(nomenclature_title)
    assert chain_link.resolve(nomenclature_title_dict) == expected


@pytest.mark.parametrize(
    "nomenclature_title, expected",
    [
        (
            "M-41-Б",
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
def test_500k(nomenclature_title, expected):
    chain_link, nomenclature_title_dict = nomenclature_title_resolver.parse_nomenclature_string(nomenclature_title)
    assert chain_link.resolve(nomenclature_title_dict) == expected


@pytest.mark.parametrize(
    "nomenclature_title, expected",
    [
        (
            "III-M-41",
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
def test_300k(nomenclature_title, expected):
    chain_link, nomenclature_title_dict = nomenclature_title_resolver.parse_nomenclature_string(nomenclature_title)
    assert chain_link.resolve(nomenclature_title_dict) == expected
