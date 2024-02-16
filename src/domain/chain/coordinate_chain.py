from __future__ import annotations

import abc

from domain.enums import Scale
from domain.models import CoordinatePair, Nomenclature
from domain.types import NomenclatureTitleFormatter


class ICoordinateChainLink(abc.ABC):
    """Nomenclature chain for current scale."""

    previous_link: type[ICoordinateChainLink]
    outbound_class: type[ICoordinateChainLink]
    scale: Scale
    name: str
    parts: int
    alphabet: list[str]
    title_formatter: NomenclatureTitleFormatter

    @classmethod
    @abc.abstractmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        ...
