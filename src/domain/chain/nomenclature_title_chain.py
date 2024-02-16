from __future__ import annotations

import abc

from domain.enums import Scale
from domain.models import Nomenclature
from domain.types import NomenclatureTitleDictType, NomenclatureTitleFormatter


class INomenclatureTitleChainLink(abc.ABC):
    """Nomenclature chain for current scale."""

    previous_link: type[INomenclatureTitleChainLink]
    outbound_class: type[INomenclatureTitleChainLink]
    scale: Scale
    name: str
    parts: int
    alphabet: list[str]
    title_formatter: NomenclatureTitleFormatter

    @classmethod
    @abc.abstractmethod
    def resolve(
        cls,
        nomenclature_dict: NomenclatureTitleDictType,
    ) -> dict[Scale, Nomenclature]:
        ...
