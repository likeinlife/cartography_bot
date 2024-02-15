from domain.facades import INomenclatureFacade
from domain.models import CoordinatePair, Nomenclature
from domain.types import ImageType


class NomenclatureFacade(INomenclatureFacade):
    def generate_from_coordinates(self, coordinates: CoordinatePair, needed_scale: int) -> list[ImageType]:
        raise NotImplementedError

    def generate_from_nomenclature(self, nomenclature: str) -> list[ImageType]:
        raise NotImplementedError


class ImageFacade:
    def generate(self, nomenclature_list: list[Nomenclature]) -> list[ImageType]:
        raise NotImplementedError
