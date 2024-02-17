from typing import Callable

from domain.facades import INomenclatureFacade

from cartography.chain.interfaces import ICoordinateChainLink, INomenclatureTitleChainLink
from cartography.enums import Scale
from cartography.models import CoordinatePair, Nomenclature
from cartography.scale_resolver import (
    coordinate_chain_link_resolver,
    coordinate_resolver,
    nomenclature_title_chain_link_resolver,
    nomenclature_title_resolver,
)
from cartography.types import ImageType


class NomenclatureFacade(INomenclatureFacade):
    @staticmethod
    def generate_from_coordinates(coordinate_pair: CoordinatePair, needed_scale: int) -> list[ImageType]:
        chain_link = coordinate_resolver.get_scale(needed_scale)
        nomenclatures_dict = chain_link.resolve(coordinate_pair)
        return _generate_image_list(nomenclatures_dict, coordinate_chain_link_resolver.get_chain_link)

    @staticmethod
    def generate_from_nomenclature(nomenclature: str) -> list[ImageType]:
        chain_link, nomenclature_title_dict = nomenclature_title_resolver.parse_nomenclature_string(nomenclature)
        nomenclatures_dict = chain_link.resolve(nomenclature_title_dict)

        return _generate_image_list(
            nomenclatures_dict,
            nomenclature_title_chain_link_resolver.get_chain_link,
        )


def _generate_image_list(
    nomenclature_dict: dict[Scale, Nomenclature],
    resolver: Callable[[Scale], type[ICoordinateChainLink | INomenclatureTitleChainLink]],
) -> list[ImageType]:
    from .image_facade import ImageGeneratorFacade

    images: list[ImageType] = []
    for scale, nomenclature in nomenclature_dict.items():
        cur_chain_link = resolver(scale)

        outbound = cur_chain_link.previous_link

        if outbound:
            outbound_nomenclature = nomenclature_dict[outbound.scale]
            outbound_info = resolver(outbound.scale)
            outer_title = f"{outbound_nomenclature.title} ({outbound_info.name})"
            images.append(
                ImageGeneratorFacade.generate(
                    upper_bound=nomenclature.outer_upper_bound,
                    lower_bound=nomenclature.outer_lower_bound,
                    cell_to_fill=nomenclature.cell_to_fill,
                    title=outer_title,
                    parts=cur_chain_link.parts,
                    alphabet=cur_chain_link.alphabet,
                )
            )

        title = f"{nomenclature.title} ({cur_chain_link.name})"
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
