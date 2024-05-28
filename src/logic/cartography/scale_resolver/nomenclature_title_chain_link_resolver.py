from logic.cartography.chain import nomenclature_title_chain
from logic.cartography.chain.interfaces import INomenclatureTitleChainLink
from logic.cartography.enums import Scale

chain_list: list[type[INomenclatureTitleChainLink]] = [
    nomenclature_title_chain.ChainLink1M,
    nomenclature_title_chain.ChainLink500K,
    nomenclature_title_chain.ChainLink300K,
    nomenclature_title_chain.ChainLink200K,
    nomenclature_title_chain.ChainLink100K,
    nomenclature_title_chain.ChainLink50K,
    nomenclature_title_chain.ChainLink25K,
    nomenclature_title_chain.ChainLink10K,
    nomenclature_title_chain.ChainLink5K,
    nomenclature_title_chain.ChainLink2K,
]
table: dict[Scale, type[INomenclatureTitleChainLink]] = {type_.scale: type_ for type_ in chain_list}


def get_chain_link(scale: Scale) -> type[INomenclatureTitleChainLink]:
    return table[scale]
