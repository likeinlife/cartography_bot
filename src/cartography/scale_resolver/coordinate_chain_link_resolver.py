from cartography.chain import coordinate_chain
from cartography.chain.interfaces import ICoordinateChainLink
from cartography.enums import Scale

chain_list: list[type[ICoordinateChainLink]] = [
    coordinate_chain.ChainLink1M,
    coordinate_chain.ChainLink500K,
    coordinate_chain.ChainLink300K,
    coordinate_chain.ChainLink200K,
    coordinate_chain.ChainLink100K,
    coordinate_chain.ChainLink50K,
    coordinate_chain.ChainLink25K,
    coordinate_chain.ChainLink10K,
    coordinate_chain.ChainLink5K,
    coordinate_chain.ChainLink2K,
]
table: dict[Scale, type[ICoordinateChainLink]] = {type_.scale: type_ for type_ in chain_list}


def get_chain_link(scale: Scale) -> type[ICoordinateChainLink]:
    return table[scale]
