import abc

from cartography.models import CoordinatePair
from cartography.types import ImageType


class IImageGenerator(abc.ABC):
    @abc.abstractmethod
    def generate(
        self,
        upper_bound: CoordinatePair,
        lower_bound: CoordinatePair,
        cell_to_fill: str | None,
        title: str,
        parts: int,
        alphabet: list[str],
    ) -> ImageType:
        """Generate image with table and labels."""
