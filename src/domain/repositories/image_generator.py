from __future__ import annotations

import abc

from domain.models import Nomenclature
from domain.types import ImageType


class IImageGeneratorRepository(abc.ABC):
    """Nomenclature image generator."""

    @abc.abstractmethod
    def generate(
        self,
        nomenclature_list: list[Nomenclature],
    ) -> list[ImageType]:
        ...
