from domain.chain import ICoordinateChainLink

from business.chain import coordinate_chain

table: dict[int, type[ICoordinateChainLink]] = {
    1: coordinate_chain.ChainLink1M,
    2: coordinate_chain.ChainLink500K,
    3: coordinate_chain.ChainLink300K,
    4: coordinate_chain.ChainLink200K,
    5: coordinate_chain.ChainLink100K,
    6: coordinate_chain.ChainLink50K,
    7: coordinate_chain.ChainLink25K,
    8: coordinate_chain.ChainLink10K,
    9: coordinate_chain.ChainLink5K,
    10: coordinate_chain.ChainLink2K,
}


def get_scale(number: int) -> type[ICoordinateChainLink]:
    return table[number]
