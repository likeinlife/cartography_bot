from typing import Callable

from domain.chain import ICoordinateChainLink
from domain.enums import Scale
from domain.models import CoordinatePair, Nomenclature

from business import constants
from business.calculate_nomenclature import get_1m_nomenclature, get_nomenclature_by_parts


class ChainLinkShortcut(ICoordinateChainLink):
    @classmethod
    def _resolve_shortcut(
        cls,
        coordinate_pair: CoordinatePair,
        previous_scale: Scale,
        parts_number: int,
        alphabet: list[str] | None = None,
        title_formatter: Callable[[str, str], str] = lambda x, y: f"{x}-{y}",
    ) -> dict[Scale, Nomenclature]:
        previous = cls.previous_link.resolve(coordinate_pair)
        this = {
            cls.scale: get_nomenclature_by_parts(
                coordinate_pair=coordinate_pair,
                parts_number=parts_number,
                previous_nomenclature=previous[previous_scale],
                alphabet=alphabet,
                title_formatter=title_formatter,
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
            parts_number=2,
            alphabet=constants.UPPER_ALPHA,
        )


class ChainLink300K(ChainLinkShortcut, ICoordinateChainLink):
    previous_link = ChainLink500K
    scale = Scale._300K

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        title_formatter = lambda x, y: f"{y}-{x}"

        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale=ChainLink1M.scale,
            parts_number=3,
            title_formatter=title_formatter,
            alphabet=constants.ROMAN,
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
            parts_number=6,
            alphabet=constants.ROMAN,
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
            parts_number=12,
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
            parts_number=2,
            alphabet=constants.UPPER_ALPHA,
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
            parts_number=2,
            alphabet=constants.LOWER_ALPHA,
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
            parts_number=2,
        )


class ChainLink5K(ChainLinkShortcut, ICoordinateChainLink):
    previous_link = ChainLink10K
    scale = Scale._5K

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        title_formatter = lambda x, y: f"{x}-({y})"
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale=cls.previous_link.scale,
            parts_number=16,
            title_formatter=title_formatter,
        )


class ChainLink2K(ChainLinkShortcut, ICoordinateChainLink):
    previous_link = ChainLink5K
    scale = Scale._2K

    @classmethod
    def resolve(
        cls,
        coordinate_pair: CoordinatePair,
    ) -> dict[Scale, Nomenclature]:
        title_formatter = lambda x, y: f"{x}-({y})"
        return cls._resolve_shortcut(
            coordinate_pair=coordinate_pair,
            previous_scale=cls.previous_link.scale,
            parts_number=3,
            alphabet=constants.LOWER_ALPHA_EXTENDED,
            title_formatter=title_formatter,
        )
