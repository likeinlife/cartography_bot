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

            previous_scale = scale_info.class_.previous_link

            if previous_scale:
                previous_scale_nomenclature = nomenclatures_dict[previous_scale.scale]
                previous_scale_info = scale_info_resolver.get_scale_info(previous_scale.scale)
                outer_title = f"{previous_scale_nomenclature.title} ({previous_scale_info.name})"
                images.append(
                    ImageGeneratorFacade.generate(
                        upper_bound=nomenclature.outer_upper_bound,
                        lower_bound=nomenclature.outer_lower_bound,
                        cell_to_fill=nomenclature.cell_to_fill,
                        title=outer_title,
                        parts=scale_info.parts,
                        alphabet=scale_info.alphabet,
                    )
                )

            title = f"{nomenclature.title} ({scale_info.name})"
            images.append(
                ImageGeneratorFacade.generate(
                    upper_bound=nomenclature.upper_bound,
                    lower_bound=nomenclature.lower_bound,
                    cell_to_fill=None,
                    title=title,
                    parts=1,
                    alphabet=[" "],
                )
            )
        return images

    @classmethod
    def generate_from_nomenclature(cls, nomenclature: str) -> list[ImageType]:
        raise NotImplementedError
