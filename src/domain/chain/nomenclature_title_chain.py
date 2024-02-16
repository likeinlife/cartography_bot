from __future__ import annotations

import abc

from domain.enums import Scale
from domain.models import Nomenclature
from domain.types import NomenclatureTitleDictType


class INomenclatureTitleChainLink(abc.ABC):
    """Nomenclature chain for current scale."""

    previous_link: type[INomenclatureTitleChainLink]
    scale: Scale

    @classmethod
    @abc.abstractmethod
    def resolve(
        cls,
        nomenclature_dict: NomenclatureTitleDictType,
    ) -> dict[Scale, Nomenclature]:
        ...
