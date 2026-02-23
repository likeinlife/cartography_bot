import abc

from logic.cartography.types import ImageType

from domain.models.coordinate_pair import CoordinatePair


class INomenclatureFacade(abc.ABC):
    """Facade for image generation from nomenclature and coordinates."""

    @abc.abstractmethod
    def generate_from_coordinates(self, coordinate_pair: CoordinatePair, needed_scale: int) -> list[ImageType]: ...

    @abc.abstractmethod
    def generate_from_nomenclature(self, nomenclature: str) -> list[ImageType]: ...
