import abc

from domain.models import CoordinatePair

from .types import ImageType


class INomenclatureFacade(abc.ABC):
    """Facade for image generation from nomenclature and coordinates."""

    @classmethod
    @abc.abstractmethod
    def generate_from_coordinates(cls, coordinate_pair: CoordinatePair, needed_scale: int) -> list[ImageType]:
        ...

    @classmethod
    @abc.abstractmethod
    def generate_from_nomenclature(cls, nomenclature: str) -> list[ImageType]:
        ...
