from __future__ import annotations

import abc

from domain.models import CoordinatePair, Nomenclature


class IChainLink(abc.ABC):
    """Nomenclature chain for current scale."""

    previous_link: type[IChainLink]
    scale: str

    @abc.abstractmethod
    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[str, Nomenclature]:
        ...
