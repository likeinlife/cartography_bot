from domain.chain import IChainLink

from src.domain.models import CoordinatePair, Nomenclature


class ChainLink1M(IChainLink):
    previous_link = None

    def resolve(
        self,
        coordinate_pair: CoordinatePair,
        previous_nomenclature_list: list[Nomenclature] | None = None,
    ) -> list[Nomenclature]:
        ...


class ChainLink500K(IChainLink):
    previous_link = ChainLink1M

    def resolve(
        self,
        coordinate_pair: CoordinatePair,
        previous_nomenclature_list: list[Nomenclature] | None = None,
    ) -> list[Nomenclature]:
        ...
