import re

from domain.chain.nomenclature_title_chain import INomenclatureTitleChainLink
from domain.enums import Scale
from domain.types import NomenclatureTitleDictType
from errors import InvalidNomenclatureTitleError

from business.scale_resolver import nomenclature_title_chain_link_resolver as chain_link_resolver

re_group_resolver = {
    "m1": Scale._1M,
    "k500": Scale._500K,
    "k300": Scale._300K,
    "k200": Scale._200K,
    "k100": Scale._100K,
    "k50": Scale._50K,
    "k25": Scale._25K,
    "k10": Scale._10K,
    "k5": Scale._5K,
    "k2": Scale._2K,
}

patterns = {
    Scale._1M: r"(?P<m1>[A-Z]-[0-9]{1,2})",
    Scale._500K: r"(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k500>[А-Г])",
    Scale._300K: r"(?P<k300>[IVX]{1,4})-(?P<m1>[A-Z]-[0-9]{1,2})",
    Scale._200K: r"(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k200>[IVX]{1,6})",
    Scale._100K: r"(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})",
    Scale._50K: r"(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})-(?P<k50>[А-Г])",
    Scale._25K: r"(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})-(?P<k50>[А-Г])-(?P<k25>[а-г])",
    Scale._10K: r"(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})-(?P<k50>[А-Г])-(?P<k25>[а-г])-(?P<k10>[0-4])",
    Scale._5K: r"(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})-\((?P<k5>[0-9]{1,3})\)",
    Scale._2K: r"(?P<m1>[A-Z]-[0-9]{1,2})-(?P<k100>[0-9]{1,3})-\((?P<k5>[0-9]{1,3})\)-\((?P<k2>[а-и])\)",
}


def _transform_re_groupdict(groupdict: dict[str, str]) -> NomenclatureTitleDictType:
    return {re_group_resolver[key]: value for key, value in groupdict.items()}


def _match(
    nomenclature_title: str,
    chain_link: type[INomenclatureTitleChainLink],
) -> tuple[type[INomenclatureTitleChainLink], NomenclatureTitleDictType] | None:
    if re_match := re.fullmatch(patterns[chain_link.scale], nomenclature_title):
        return (chain_link, _transform_re_groupdict(re_match.groupdict()))
    return None


def parse_nomenclature_string(
    nomenclature_title: str,
) -> tuple[type[INomenclatureTitleChainLink], NomenclatureTitleDictType]:
    """Parse nomenclature string."""
    for chain_link in chain_link_resolver.chain_list:
        if result := _match(nomenclature_title, chain_link):
            return result
    raise InvalidNomenclatureTitleError
