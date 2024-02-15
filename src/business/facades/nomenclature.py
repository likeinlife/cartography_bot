from domain.facades import INomenclatureFacade
from domain.models import CoordinatePair
from domain.types import ImageType

from business.scale_resolver import coordinate_resolver


class NomenclatureFacade(INomenclatureFacade):
    def generate_from_coordinates(self, coordinate_pair: CoordinatePair, needed_scale: int) -> list[ImageType]:
        chain_link = coordinate_resolver.get_scale(needed_scale)
        chain_link.resolve(coordinate_pair)

    def generate_from_nomenclature(self, nomenclature: str) -> list[ImageType]:
        raise NotImplementedError
