from __future__ import annotations

import abc

from domain.enums import Scale
from domain.models import CoordinatePair, Nomenclature


class ICoordinateChainLink(abc.ABC):
    """Nomenclature chain for current scale."""

    previous_link: type[ICoordinateChainLink]
    scale: Scale

    @classmethod
    @abc.abstractmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        ...
