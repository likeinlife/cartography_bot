from domain.facades import INomenclatureFacade
from domain.models import CoordinatePair
from domain.types import ImageType

from business.scale_resolver import coordinate_resolver, scale_info_resolver

from .image import ImageGeneratorFacade


class NomenclatureFacade(INomenclatureFacade):
    @classmethod
    def generate_from_coordinates(cls, coordinate_pair: CoordinatePair, needed_scale: int) -> list[ImageType]:
        chain_link = coordinate_resolver.get_scale(needed_scale)
        nomenclatures_dict = chain_link.resolve(coordinate_pair)
        images: list[ImageType] = []
        for scale, nomenclature in nomenclatures_dict.items():
            scale_info = scale_info_resolver.get_scale_info(scale)
            images.append(
                ImageGeneratorFacade.generate(
                    nomenclature=nomenclature,
                    scale_name=scale_info.name,
                    parts=scale_info.parts,
                    alphabet=scale_info.alphabet,
                )
            )
        return images

    @classmethod
    def generate_from_nomenclature(cls, nomenclature: str) -> list[ImageType]:
        raise NotImplementedError
