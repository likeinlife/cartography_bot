from __future__ import annotations

import abc

from domain.models import CoordinatePair, Nomenclature


class IChainLink(abc.ABC):
    """Nomenclature chain for current scale."""

    previous_link: type[IChainLink] | None = None

    @abc.abstractmethod
    def resolve(
        self,
        coordinate_pair: CoordinatePair,
        previous_nomenclature_list: list[Nomenclature] | None = None,
    ) -> list[Nomenclature]:
        ...
