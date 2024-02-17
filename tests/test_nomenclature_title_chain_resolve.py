import pytest
from business.chain import nomenclature_title_chain as chain
from business.scale_resolver import nomenclature_title_resolver as resolver


@pytest.mark.parametrize(
    "nomenclature_title, expected",
    [
        ("I-31", chain.ChainLink1M),
        ("I-31-А", chain.ChainLink500K),
        ("III-I-31", chain.ChainLink300K),
        ("I-31-VIII", chain.ChainLink200K),
        ("M-42-39", chain.ChainLink100K),
        ("M-42-39-Б", chain.ChainLink50K),
        ("M-42-39-Б-в", chain.ChainLink25K),
        ("M-42-39-Б-в-2", chain.ChainLink10K),
        ("M-42-39-(75)", chain.ChainLink5K),
        ("M-42-39-(75)-(б)", chain.ChainLink2K),
    ],
)
def test_nomenclature_title_chain_resolve(nomenclature_title, expected):
    assert resolver.parse_nomenclature_string(nomenclature_title)[0] == expected
