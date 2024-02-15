from domain.chain import ICoordinateChainLink
from domain.enums import Scale
from domain.models import CoordinatePair, Nomenclature

from business.calculate_nomenclature import get_1m_nomenclature, get_nomenclature_by_parts
from business.scale_resolver.scale_info_resolver import get_scale_info


class ChainLinkShortcut(ICoordinateChainLink):
    @classmethod
    def _resolve_shortcut(
        cls,
        coordinate_pair: CoordinatePair,
        previous_scale: Scale,
    ) -> dict[Scale, Nomenclature]:
        previous = cls.previous_link.resolve(coordinate_pair)
        scale_info = get_scale_info(scale=cls.scale)
        this = {
            cls.scale: get_nomenclature_by_parts(
                coordinate_pair=coordinate_pair,
                parts_number=scale_info.parts,
                previous_nomenclature=previous[previous_scale],
                alphabet=scale_info.alphabet,
                title_formatter=scale_info.formatter,
            )
        }
        return previous | this


class ChainLink1M(ICoordinateChainLink):
    previous_link = None  # type: ignore
    scale = Scale._1M

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        return {cls.scale: get_1m_nomenclature(coordinate_pair)}


class ChainLink500K(ChainLinkShortcut, ICoordinateChainLink):
    previous_link = ChainLink1M
    scale = Scale._500K

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale=ChainLink1M.scale,
        )


class ChainLink300K(ChainLinkShortcut, ICoordinateChainLink):
    previous_link = ChainLink500K
    scale = Scale._300K

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale=ChainLink1M.scale,
        )


class ChainLink200K(ChainLinkShortcut, ICoordinateChainLink):
    previous_link = ChainLink300K
    scale = Scale._200K

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale=ChainLink1M.scale,
        )


class ChainLink100K(ChainLinkShortcut, ICoordinateChainLink):
    previous_link = ChainLink200K
    scale = Scale._100K

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale=ChainLink1M.scale,
        )


class ChainLink50K(ChainLinkShortcut, ICoordinateChainLink):
    previous_link = ChainLink100K
    scale = Scale._50K

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale=cls.previous_link.scale,
        )


class ChainLink25K(ChainLinkShortcut, ICoordinateChainLink):
    previous_link = ChainLink50K
    scale = Scale._25K

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale=cls.previous_link.scale,
        )


class ChainLink10K(ChainLinkShortcut, ICoordinateChainLink):
    previous_link = ChainLink25K
    scale = Scale._10K

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale=cls.previous_link.scale,
        )


class ChainLink5K(ChainLinkShortcut, ICoordinateChainLink):
    previous_link = ChainLink10K
    scale = Scale._5K

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale=cls.previous_link.scale,
        )


class ChainLink2K(ChainLinkShortcut, ICoordinateChainLink):
    previous_link = ChainLink5K
    scale = Scale._2K

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale=cls.previous_link.scale,
        )
