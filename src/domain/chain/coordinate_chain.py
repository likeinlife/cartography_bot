from __future__ import annotations

import abc

from domain.models import CoordinatePair, Nomenclature


class ICoordinateChainLink(abc.ABC):
    """Nomenclature chain for current scale."""

    previous_link: type[ICoordinateChainLink]
    scale: str

    @classmethod
    @abc.abstractmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[str, Nomenclature]:
        ...
