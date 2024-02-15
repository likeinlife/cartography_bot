from domain.facades import INomenclatureFacade
from domain.models import CoordinatePair
from domain.types import ImageType


class NomenclatureFacade(INomenclatureFacade):
    def generate_from_coordinates(self, coordinates: CoordinatePair, needed_scale: int) -> list[ImageType]:
        raise NotImplementedError

    def generate_from_nomenclature(self, nomenclature: str) -> list[ImageType]:
        raise NotImplementedError
