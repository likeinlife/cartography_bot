import abc

from business.types import ImageType

from domain.models import CoordinatePair


class INomenclatureFacade(abc.ABC):
    """Facade for image generation from nomenclature and coordinates."""

    @staticmethod
    @abc.abstractmethod
    def generate_from_coordinates(coordinate_pair: CoordinatePair, needed_scale: int) -> list[ImageType]:
        ...

    @staticmethod
    @abc.abstractmethod
    def generate_from_nomenclature(nomenclature: str) -> list[ImageType]:
        ...
